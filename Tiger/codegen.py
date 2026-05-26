
from __future__ import annotations
from enum import member
from typing import List, Optional, Set
import os
import ast_nodes as A
from type_checker import type_to_cpp



_RUNTIME_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "runtime")


def _load_runtime(rel_path: str) -> str:
    full = os.path.normpath(os.path.join(_RUNTIME_DIR, rel_path))
    try:
        with open(full, "r", encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        raise FileNotFoundError(
            f"Tiger runtime file missing: {full}\n"
            f"  Expected layout:  runtime/{rel_path}\n"
            f"  (Re-clone or restore the Tiger SDK to fix this.)"
        )



class _Templates:
    _cache: dict = {}

    _SINGLE: dict = {
        "std_headers": "std_headers.hpp",
        "tiger_rt":    "tiger_rt.hpp",
        "cli":         "cli/cli.hpp",
        "http":        "http/http.hpp",
        "time":        "time/time.hpp",
        "random":      "random/random.hpp",
        "files":       "files/files.hpp",
    }

    _GUI_ORDER = [
        "gui/types.hpp",
        "gui/events.hpp",
        "gui/window.hpp",
        "gui/button.hpp",
        "gui/label.hpp",
        "gui/entry.hpp",
        "gui/run.hpp",
        "gui/enhanced_button.hpp",
        "gui/enhanced_label.hpp",
    ]

    def __getattr__(self, name: str) -> str:
        if name not in self._cache:
            if name in self._SINGLE:
                self._cache[name] = _load_runtime(self._SINGLE[name])
            elif name == "gui":
                parts = [_load_runtime(f) for f in self._GUI_ORDER]
                self._cache[name] = "\n".join(parts)
            else:
                raise AttributeError(f"Unknown runtime template: {name!r}")
        return self._cache[name]


_T = _Templates()

BUILTIN_MODULES: Set[str] = {"http", "gui", "random", "time", "files", "cli"}



def _needs_rt(node: A.Node) -> bool:
    if isinstance(node, A.ListLit):
        return True
    if isinstance(node, A.DictLit):
        return True
    if isinstance(node, A.Call):
        if isinstance(node.callee, A.MemberAccess):
            obj = node.callee.obj
            if isinstance(obj, A.Ident) and obj.name == "str":
                return True
    for attr in vars(node).values():
        if isinstance(attr, A.Node) and _needs_rt(attr):
            return True
        if isinstance(attr, list):
            for item in attr:
                if isinstance(item, A.Node) and _needs_rt(item):
                    return True
    return False


def _program_needs_rt(program: A.Program) -> bool:
    for stmt in program.stmts:
        if _needs_rt(stmt):
            return True
    return False



def _infer_global_type(node: A.Node) -> str:
    if isinstance(node, A.IntLit):
        return "int"
    if isinstance(node, A.FloatLit):
        return "double"
    if isinstance(node, A.StringLit):
        return "std::string"
    if isinstance(node, A.BoolLit):
        return "bool"
    if isinstance(node, A.NullLit):
        return "void*"
    if isinstance(node, A.ListLit):
        return "std::vector<double>"
    if isinstance(node, A.DictLit):
        return "std::map<std::string, std::any>"
    if isinstance(node, A.Call):
        if isinstance(node.callee, A.MemberAccess):
            obj = node.callee.obj
            member = node.callee.member
            if isinstance(obj, A.Ident) and obj.name == "files":
                if member == "read":
                    return "std::string"
                if member == "list_dir":
                    return "std::vector<std::string>"
    return "double"



class GenError(Exception):
    def __init__(self, msg: str, line: int = 0):
        super().__init__(f"GenError at line {line}: {msg}")


class CodeGen:
    def __init__(self):
        self._indent       = 0
        self._lines:        List[str] = []
        self._imports:      Set[str]  = set()   
        self._tgr_imports:  List[str] = []      
        self._need_rt:      bool      = False
        self._in_main:      bool      = False   


    def _emit(self, code: str):
        self._lines.append("    " * self._indent + code)

    def _blank(self):
        self._lines.append("")


    def generate(self, program: A.Program,
                 injected_stmts: Optional[List[A.Node]] = None) -> str:
        injected_stmts = injected_stmts or []

        self._collect_imports(program)

        self._need_rt = (
            _program_needs_rt(program) or
            any(_needs_rt(n) for n in injected_stmts)
        )

        preamble = [_T.std_headers]
        if self._need_rt:
            preamble.append(_T.tiger_rt)
        if "http" in self._imports:
            preamble.append(_T.http)
        if "gui" in self._imports:
            preamble.append(_T.gui)
        if "random" in self._imports:
            preamble.append(_T.random)
        if "time" in self._imports:
            preamble.append(_T.time)
        if "files" in self._imports:
            preamble.append(_T.files)
        if "cli" in self._imports:
            preamble.append(_T.cli)
        has_cli = "cli" in self._imports

        inj_globals = [s for s in injected_stmts if isinstance(s, A.VarDecl)]
        inj_funcs   = [s for s in injected_stmts if isinstance(s, A.FuncDef)]

        top_globals = [s for s in program.stmts
                       if isinstance(s, A.VarDecl)]
        non_main    = [s for s in program.stmts
                       if isinstance(s, A.FuncDef) and s.name != "main"]
        main_fn     = next((s for s in program.stmts
                            if isinstance(s, A.FuncDef) and s.name == "main"), None)
        top_stmts   = [s for s in program.stmts
                       if not isinstance(s, A.FuncDef)
                       and not isinstance(s, A.ImportStmt)
                       and not isinstance(s, A.VarDecl)]

        all_globals = inj_globals + top_globals   
        all_funcs   = inj_funcs   + non_main       

        global_lines: List[str] = []
        cli_globals = []  
        for gvar in all_globals:
            if has_cli and gvar.value and self._uses_cli(gvar.value):
                cli_globals.append(gvar)
            else:
                global_lines.append(self._gen_global_var(gvar))
        if global_lines:
            global_lines.append("")   

        # NOTE: `auto` return type cannot be forward-declared before C++20.
        fwd_lines: List[str] = []   

        body_lines: List[str] = []
        for fn in all_funcs:
            self._lines  = []
            self._indent = 0
            self._gen_func(fn)
            body_lines += self._lines
            body_lines.append("")

        self._lines  = []
        self._indent = 0
        has_cli = "cli" in self._imports
        if main_fn:
            if has_cli:
                self._in_main = True
                self._emit("int main(int argc, char* argv[]) {")
                self._indent += 1
                self._emit("tiger_cli::parse_args(argc, argv);")
                for gvar in cli_globals:
                    self._emit(f"{self._gen_global_var(gvar)}")
                for s in main_fn.body:
                    self._gen_stmt(s)
                if not isinstance(main_fn.body[-1], A.ReturnStmt):
                    self._emit("return 0;")
                self._in_main = False
                self._indent -= 1
                self._emit("}")
            else:
                self._gen_func(main_fn, force_int=True)
        else:
            if has_cli:
                self._in_main = True
                self._emit("int main(int argc, char* argv[]) {")
                self._indent += 1
                self._emit("tiger_cli::parse_args(argc, argv);")
                for gvar in cli_globals:
                    self._emit(self._gen_global_var(gvar))
                for s in top_stmts:
                    self._gen_stmt(s)
                self._in_main = False
                self._emit("return 0;")
                self._indent -= 1
                self._emit("}")
            else:
                self._in_main = True
                self._emit("int main() {")
                self._indent += 1
                for s in top_stmts:
                    self._gen_stmt(s)
                self._in_main = False
                self._emit("return 0;")
                self._indent -= 1
                self._emit("}")
        body_lines += self._lines

        parts: List[str] = preamble + [""]
        if global_lines:
            parts += global_lines
        if fwd_lines:
            parts += fwd_lines + [""]
        parts += body_lines
        return "\n".join(parts)


    def _collect_imports(self, program: A.Program):
        seen_tgr: List[str] = []
        for node in program.stmts:
            if not isinstance(node, A.ImportStmt):
                continue
            mod = node.module
            if mod in BUILTIN_MODULES:
                self._imports.add(mod)
            else:
                if mod not in seen_tgr:
                    seen_tgr.append(mod)
        self._tgr_imports = seen_tgr


    def _gen_global_var(self, node: A.VarDecl) -> str:
            if node.type_name:
                cpp_type = type_to_cpp(node.type_name)
                if node.value is None:
                    if "vector" in cpp_type:
                        return f"{cpp_type} {node.name} = {{}};"
                    return f"{cpp_type} {node.name};"
            else:
                if node.value is None:
                    return f"double {node.name} = 0;"
            
            cpp_type = type_to_cpp(node.type_name) if node.type_name else _infer_global_type(node.value)
            cpp_val  = self._gen_expr(node.value) if node.value else "{}"
            
            if isinstance(node.value, A.ListLit) and not node.value.elements:
                return f"std::vector<double> {node.name} = {{}};"
            
            return f"{cpp_type} {node.name} = {cpp_val};"
        
    def _uses_cli(self, node: A.Node) -> bool:
        if isinstance(node, A.Call):
            if isinstance(node.callee, A.MemberAccess):
                obj = node.callee.obj
                if isinstance(obj, A.Ident) and obj.name == "cli":
                    return True
        for attr in vars(node).values():
            if isinstance(attr, A.Node) and self._uses_cli(attr):
                return True
            if isinstance(attr, list):
                for item in attr:
                    if isinstance(item, A.Node) and self._uses_cli(item):
                        return True
        return False

    def _params_str(self, params: List[str], param_types: List[Optional[str]]) -> str:
        items = []
        for i, p in enumerate(params):
            ptype = param_types[i] if i < len(param_types) else None
            if ptype:
                items.append(f"{type_to_cpp(ptype)} {p}")
            else:
                items.append(f"auto {p}")
        return ", ".join(items)

    def _gen_func(self, fn: A.FuncDef, force_int: bool = False):
        if fn.name == "main" or force_int:
            sig = "int main()"
            self._in_main = True
        else:
            return_type = type_to_cpp(fn.return_type) if fn.return_type else "auto"
            sig = f"{return_type} {fn.name}({self._params_str(fn.params, fn.param_types)})"
            self._in_main = False
        self._emit(f"{sig} {{")
        self._indent += 1
        for s in fn.body:
            self._gen_stmt(s)
        if fn.name == "main" or force_int:
            if not fn.body or not isinstance(fn.body[-1], A.ReturnStmt):
                self._emit("return 0;")
            self._in_main = False
        self._indent -= 1
        self._emit("}")


    def _gen_stmt(self, node: A.Node):
        if isinstance(node, A.VarDecl):
            self._gen_var_decl(node)
        elif isinstance(node, A.Assign):
            self._gen_assign(node)
        elif isinstance(node, A.PrintStmt):
            self._gen_print(node)
        elif isinstance(node, A.ReturnStmt):
            self._gen_return(node)
        elif isinstance(node, A.IfStmt):
            self._gen_if(node)
        elif isinstance(node, A.WhileStmt):
            self._gen_while(node)
        elif isinstance(node, A.ForStmt):
            self._gen_for(node)
        elif isinstance(node, A.ExprStmt):
            self._emit(f"{self._gen_expr(node.expr)};")
        elif isinstance(node, A.ImportStmt):
            pass   
        elif isinstance(node, A.FuncDef):
            raise GenError("Nested function definitions are not supported", node.line)
        else:
            raise GenError(
                f"Unknown statement node: {type(node).__name__}",
                getattr(node, "line", 0)
            )

    def _gen_var_decl(self, node: A.VarDecl):
        if node.type_name:
            cpp_type = type_to_cpp(node.type_name)
            if node.value is None:
                self._emit(f"{cpp_type} {node.name};")
            else:
                self._emit(f"{cpp_type} {node.name} = {self._gen_expr(node.value)};")
        else:
            if node.value is None:
                self._emit(f"auto {node.name} = 0;")
            else:
                self._emit(f"auto {node.name} = {self._gen_expr(node.value)};")

    def _gen_assign(self, node: A.Assign):
        self._emit(f"{self._gen_expr(node.target)} {node.op} {self._gen_expr(node.value)};")

    def _gen_print(self, node: A.PrintStmt):
        if not node.args:
            self._emit("std::cout << std::endl;")
            return
        parts = []
        for i, arg in enumerate(node.args):
            parts.append(self._gen_expr(arg))
            if i < len(node.args) - 1:
                parts.append('" "')
        self._emit(f"std::cout << {' << '.join(parts)} << std::endl;")

    def _gen_return(self, node: A.ReturnStmt):
            if node.value is None:
                if self._in_main:
                    self._emit("return 0;")
                else:
                    self._emit("return;")
            else:
                self._emit(f"return {self._gen_expr(node.value)};")

    def _gen_if(self, node: A.IfStmt):
        self._emit(f"if ({self._gen_expr(node.condition)}) {{")
        self._indent += 1
        for s in node.then_body:
            self._gen_stmt(s)
        self._indent -= 1
        for ec in node.elif_clauses:
            self._emit(f"}} else if ({self._gen_expr(ec.condition)}) {{")
            self._indent += 1
            for s in ec.body:
                self._gen_stmt(s)
            self._indent -= 1
        if node.else_body is not None:
            self._emit("} else {")
            self._indent += 1
            for s in node.else_body:
                self._gen_stmt(s)
            self._indent -= 1
        self._emit("}")

    def _gen_while(self, node: A.WhileStmt):
        self._emit(f"while ({self._gen_expr(node.condition)}) {{")
        self._indent += 1
        for s in node.body:
            self._gen_stmt(s)
        self._indent -= 1
        self._emit("}")

    def _gen_for(self, node: A.ForStmt):
        iterable = self._gen_expr(node.iterable)
        self._emit(f"for (const auto& {node.var} : {iterable}) {{")
        self._indent += 1
        for s in node.body:
            self._gen_stmt(s)
        self._indent -= 1
        self._emit("}")


    def _gen_expr(self, node: A.Node) -> str:
        if isinstance(node, A.IntLit):
            return str(node.value)
        if isinstance(node, A.FloatLit):
            s = repr(node.value)
            return s if ("." in s or "e" in s) else s + ".0"
        if isinstance(node, A.StringLit):
            esc = (node.value
                   .replace("\\", "\\\\")
                   .replace('"',  '\\"')
                   .replace("\n", "\\n")
                   .replace("\t", "\\t")
                   .replace("\r", "\\r"))
            return f'std::string("{esc}")'
        if isinstance(node, A.BoolLit):
            return "true" if node.value else "false"
        if isinstance(node, A.NullLit):
            return "nullptr"
        if isinstance(node, A.Ident):
            return node.name
        if isinstance(node, A.BinOp):
            return f"({self._gen_expr(node.left)} {node.op} {self._gen_expr(node.right)})"
        if isinstance(node, A.UnaryOp):
            return f"({node.op}{self._gen_expr(node.operand)})"
        if isinstance(node, A.Call):
            return self._gen_call(node)
        if isinstance(node, A.MemberAccess):
            return f"{self._gen_expr(node.obj)}.{node.member}"
        if isinstance(node, A.Index):
            return f"{self._gen_expr(node.obj)}[{self._gen_expr(node.index)}]"
        if isinstance(node, A.ListLit):
            return self._gen_list(node)
        if isinstance(node, A.DictLit):
            return self._gen_dict(node)
        if isinstance(node, A.InputExpr):
            return self._gen_input(node)
        if isinstance(node, A.Assign):
            return f"({self._gen_expr(node.target)} {node.op} {self._gen_expr(node.value)})"
        raise GenError(
            f"Unknown expression node: {type(node).__name__}",
            getattr(node, "line", 0)
        )


    def _gen_list(self, node: A.ListLit) -> str:
        if not node.elements:
            return "tiger_rt::make_vec<int>()"
        args = ", ".join(self._gen_expr(e) for e in node.elements)
        return f"tiger_rt::make_vec({args})"

    def _gen_dict(self, node: A.DictLit) -> str:
        if not node.keys:
            return "{}"
        pairs = []
        for k, v in zip(node.keys, node.values):
            k_str = self._gen_expr(k)
            v_str = self._gen_expr(v)
            pairs.append(f"{{{k_str}, std::any({v_str})}}")
        return "std::map<std::string, std::any>{" + ", ".join(pairs) + "}"


    def _gen_call(self, node: A.Call) -> str:
        args_str = ", ".join(self._gen_expr(a) for a in node.args)

        if isinstance(node.callee, A.MemberAccess):
            obj    = node.callee.obj
            member = node.callee.member
            if isinstance(obj, A.Ident):
                ns = obj.name
                if ns == "http":
                    return f"tiger_http::{member}({args_str})"
                if ns == "gui":
                    return f"tiger_gui::{member}({args_str})"
                if ns == "random":
                    return f"tiger_random::{member}({args_str})"
                if ns == "time":
                    return f"tiger_time::{member}({args_str})"
                if ns == "files":
                    return f"tiger_files::{member}({args_str})"
                if ns == "cli":
                    return f"tiger_cli::{member}({args_str})"
                if ns == "str":
                    return self._gen_str_call(member, node.args)

        return f"{self._gen_expr(node.callee)}({args_str})"

    def _gen_str_call(self, method: str, args: List[A.Node]) -> str:
        if not args:
            raise GenError(f"str.{method}() requires at least one argument")

        arg0 = self._gen_expr(args[0])
        rest = ", ".join(self._gen_expr(a) for a in args[1:])
        extra = (", " + rest) if rest else ""

        dispatch = {
            "upper":    f"tiger_rt::str_upper({arg0})",
            "lower":    f"tiger_rt::str_lower({arg0})",
            "len":      f"tiger_rt::str_len({arg0})",
            "to_str":   f"tiger_rt::str_to_str({arg0})",
            "to_int":   f"tiger_rt::str_to_int({arg0})",
            "to_float": f"tiger_rt::str_to_float({arg0})",
            "trim":     f"tiger_rt::str_trim({arg0})",
            "split":    f"tiger_rt::str_split({arg0})",
            "startswith": f"tiger_rt::str_startswith({arg0}, {rest})" if rest else f"tiger_rt::str_startswith({arg0}, \"\")",
            "endswith": f"tiger_rt::str_endswith({arg0}, {rest})" if rest else f"tiger_rt::str_endswith({arg0}, \"\")",
        }
        if method in dispatch:
            return dispatch[method]
        return f"/* unknown str.{method} */ {arg0}"


    def _gen_input(self, node: A.InputExpr) -> str:
        if node.prompt:
            prompt = self._gen_expr(node.prompt)
            return (
                f"([&]() -> std::string {{ "
                f"std::cout << {prompt} << std::flush; "
                f"std::string _tgr_in; std::getline(std::cin, _tgr_in); "
                f"return _tgr_in; }})()"
            )
        return (
            "([&]() -> std::string { "
            "std::string _tgr_in; std::getline(std::cin, _tgr_in); "
            "return _tgr_in; })()"
        )
