#!/usr/bin/env python3

from __future__ import annotations
import sys
import os
import subprocess
import argparse
from typing import List, Dict, Set, Optional

from lexer   import Lexer, LexerError
from parser  import Parser, ParseError
from codegen import CodeGen, GenError, BUILTIN_MODULES
from type_checker import TypeChecker, TypeCheckError
import ast_nodes as A



MINGW_CANDIDATES = [
    "g++",
    r"C:\MinGW\bin\g++.exe",
    r"C:\mingw64\bin\g++.exe",
    r"C:\msys64\mingw64\bin\g++.exe",
    r"C:\msys64\ucrt64\bin\g++.exe",
    r"C:\Program Files\mingw-w64\x86_64-8.1.0-posix-seh-rt_v6-rev0\mingw64\bin\g++.exe",
]


def find_gpp() -> Optional[str]:
    for c in MINGW_CANDIDATES:
        try:
            r = subprocess.run([c, "--version"], capture_output=True,
                               text=True, timeout=5)
            if r.returncode == 0:
                return c
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    return None



def _parse_file(path: str) -> A.Program:
    try:
        with open(path, "r", encoding="utf-8") as f:
            source = f.read()
    except OSError as e:
        _die(f"Cannot read file: {e}")

    try:
        tokens = Lexer(source).tokenize()
    except LexerError as e:
        _die(f"[{path}] {e}")

    try:
        return Parser(tokens).parse()
    except ParseError as e:
        _die(f"[{path}] {e}")


def _die(msg: str) -> None:
    print(f"\033[91mError:\033[0m {msg}", file=sys.stderr)
    sys.exit(1)



class ImportResolver:

    def __init__(self, search_dirs: List[str], verbose: bool = False):
        self._dirs:    List[str]           = search_dirs
        self._verbose: bool                = verbose
        self._parsed:  Dict[str, A.Program] = {}   
        self._loading: Set[str]            = set()  


    def resolve(self, program: A.Program,
                origin_dir: str) -> List[A.Node]:
        result: List[A.Node] = []
        seen_modules: Set[str] = set()
        self._collect(program, origin_dir, result, seen_modules)
        return result


    def _collect(self, program: A.Program, origin_dir: str,
                 out: List[A.Node], seen: Set[str]):
        for stmt in program.stmts:
            if not isinstance(stmt, A.ImportStmt):
                continue
            mod = stmt.module
            if mod in BUILTIN_MODULES or mod in seen:
                continue
            seen.add(mod)

            abs_path = self._locate(mod, origin_dir, stmt.line)

            if abs_path in self._loading:
                _die(f"Circular import detected: '{mod}' ({abs_path})")
            self._loading.add(abs_path)

            if abs_path not in self._parsed:
                if self._verbose:
                    print(f"  [import] Parsing {abs_path}")
                self._parsed[abs_path] = _parse_file(abs_path)

            imported = self._parsed[abs_path]
            imported_dir = os.path.dirname(abs_path)

            self._collect(imported, imported_dir, out, seen)

            for node in imported.stmts:
                if isinstance(node, A.ImportStmt):
                    continue
                if isinstance(node, A.FuncDef) and node.name == "main":
                    continue
                out.append(node)

            self._loading.discard(abs_path)

    def _locate(self, mod: str, origin_dir: str, line: int) -> str:
        filename = mod + ".tgr"
        for d in [origin_dir] + self._dirs:
            candidate = os.path.normpath(os.path.join(d, filename))
            if os.path.isfile(candidate):
                return os.path.abspath(candidate)
        _die(
            f"Import error (line {line}): cannot find '{filename}'\n"
            f"  Searched in: {[origin_dir] + self._dirs}"
        )



def build(source_path: str,
           search_dirs: List[str],
           verbose: bool) -> str:

    source_path = os.path.abspath(source_path)
    origin_dir  = os.path.dirname(source_path)

    if verbose:
        print(f"[1/3] Parsing {source_path}...")
    program = _parse_file(source_path)
    if verbose:
        print(f"      {len(program.stmts)} top-level nodes.")

    if verbose:
        print(f"[2/3] Resolving imports...")
    resolver = ImportResolver([origin_dir] + search_dirs, verbose)
    injected_stmts = resolver.resolve(program, origin_dir)
    if verbose and injected_stmts:
        funcs = [n.name for n in injected_stmts if isinstance(n, A.FuncDef)]
        print(f"      Injected {len(injected_stmts)} nodes "
              f"({len(funcs)} functions: {', '.join(funcs) or 'none'})")

    if verbose:
        print(f"[2.5/3] Type checking...")
    checker = TypeChecker()
    try:
        checker.check(program, injected_stmts)
    except TypeCheckError as e:
        _die(str(e))

    if verbose:
        print(f"[3/3] Generating C++...")
    try:
        gen = CodeGen()
        cpp = gen.generate(program, injected_stmts=injected_stmts)
    except GenError as e:
        _die(str(e))

    return cpp


def compile_cpp(cpp_path: str, exe_path: str, gpp: str,
                  has_gui: bool, verbose: bool):
    cmd = [gpp, "-O2", "-s", "-w", "-o", exe_path, cpp_path, "-lwininet", "-lstdc++fs"]
    if has_gui:
        cmd += ["-mwindows"]
    if verbose:
        print(f"  g++ cmd: {' '.join(cmd)}")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("\033[91mCompilation Error:\033[0m", file=sys.stderr)
        print(r.stderr, file=sys.stderr)
        sys.exit(1)
    if r.stderr and verbose:
        print(r.stderr)



def main():
    ap = argparse.ArgumentParser(
        prog="tiger v0.4.3",
        description="Tiger Transpiler: .tgr → executable"
    )
    ap.add_argument("source")
    ap.add_argument("-o", dest="output", default=None)
    ap.add_argument("--emit-cpp", "--no-compile", action="store_true",
                    help="Save the generated .cpp and skip compilation "
                         "(advanced / debugging only)")
    ap.add_argument("--cpp-out", dest="cpp_out", default=None,
                    help="Path for the .cpp file (implies --emit-cpp)")
    ap.add_argument("-I", dest="include_dirs", action="append",
                    default=[], metavar="DIR",
                    help="Extra search directory for .tgr imports")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    if args.cpp_out:
        args.emit_cpp = True

    src = args.source
    if not os.path.isfile(src):
        _die(f"File not found: {src}")
    if not src.endswith(".tgr"):
        print(f"\033[93mWarning:\033[0m '{src}' does not end with .tgr",
              file=sys.stderr)

    base     = os.path.splitext(src)[0]
    exe_path = args.output or (base + (".exe" if sys.platform == "win32" else ""))

    cpp_src = build(src, args.include_dirs, args.verbose)

    if args.emit_cpp:
        cpp_path = args.cpp_out or (base + ".cpp")
        with open(cpp_path, "w", encoding="utf-8", errors="replace") as f:
            f.write(cpp_src)
        print(f"  C++ written: {cpp_path}")
        print("  (--emit-cpp: skipping compilation)")
        return

    import tempfile
    tmp_fd, cpp_path = tempfile.mkstemp(suffix=".cpp",
                                        prefix="_tiger_",
                                        dir=os.path.dirname(os.path.abspath(src)))
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8", errors="replace") as f:
            f.write(cpp_src)

        gpp = find_gpp()
        if gpp is None:
            print(
                "\n\033[93mWarning:\033[0m g++ not found.\n"
                "  Install MinGW-w64 and add it to PATH.\n"
                "  To inspect the generated C++, rerun with --emit-cpp.",
                file=sys.stderr
            )
            sys.exit(1)

        has_gui = "tiger_gui::" in cpp_src
        compile_cpp(cpp_path, exe_path, gpp, has_gui, args.verbose)

    finally:
        try:
            os.remove(cpp_path)
        except OSError:
            pass

    print(f"  Compiled:  {exe_path}")
    print("\nBuild successful.")


if __name__ == "__main__":
    main()
