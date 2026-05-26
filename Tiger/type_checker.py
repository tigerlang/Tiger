
from __future__ import annotations
from typing import Dict, List, Optional, Any
from enum import Enum
import ast_nodes as A


class TypeError(Enum):
    UNDEFINED_VARIABLE = "undefined variable"
    TYPE_MISMATCH = "type mismatch"
    INVALID_OPERATION = "invalid operation"
    WRONG_ARGUMENT_COUNT = "wrong number of arguments"


class TypeCheckError(Exception):
    def __init__(self, msg: str, line: int = 0):
        super().__init__(f"TypeError at line {line}: {msg}")
        self.line = line


PRIMITIVE_TYPES: Dict[str, A.Type] = {
    "int": A.TInt(),
    "float": A.TFloat(),
    "string": A.TString(),
    "bool": A.TBool(),
    "null": A.TNull(),
    "void": A.TVoid(),
}


def parse_type(type_name: str) -> A.Type:
    if type_name is None:
        return A.TAny()
    
    if type_name in PRIMITIVE_TYPES:
        return PRIMITIVE_TYPES[type_name]
    
    if type_name == "list":
        return A.TList()
    
    if type_name == "dict":
        return A.TDict()
    
    if type_name.startswith("list[") and type_name.endswith("]"):
        inner = type_name[5:-1]
        return A.TList(elem_type=parse_type(inner))
    
    return A.TAny()


def type_to_cpp(type_name: str) -> str:
    if type_name is None:
        return "auto"
    
    mapping = {
        "int": "int",
        "float": "double",
        "string": "std::string",
        "bool": "bool",
        "null": "void*",
        "void": "void",
        "list": "std::vector<double>",
        "dict": "std::map<std::string, std::any>",
    }
    
    if type_name in mapping:
        return mapping[type_name]
    
    if type_name.startswith("list[") and type_name.endswith("]"):
        inner = type_name[5:-1]
        elem_cpp = type_to_cpp(inner)
        return f"std::vector<{elem_cpp}>"
    
    return "auto"


class TypeChecker:
    def __init__(self):
        self.vars: Dict[str, A.Type] = {}
        self.funcs: Dict[str, tuple] = {}
    
    def check(self, program: A.Program, injected_stmts: List[A.Node] = None) -> None:
        injected_stmts = injected_stmts or []
        
        for stmt in injected_stmts:
            if isinstance(stmt, A.FuncDef):
                self.funcs[stmt.name] = (stmt.param_types, stmt.return_type)
        for stmt in program.stmts:
            if isinstance(stmt, A.FuncDef):
                self.funcs[stmt.name] = (stmt.param_types, stmt.return_type)
        
        for stmt in injected_stmts:
            if isinstance(stmt, A.VarDecl):
                self._check_var_decl(stmt)
            elif isinstance(stmt, A.FuncDef):
                for i, param in enumerate(stmt.params):
                    if i < len(stmt.param_types):
                        self.vars[param] = parse_type(stmt.param_types[i])
                    else:
                        self.vars[param] = A.TAny()
                for s in stmt.body:
                    self._check_stmt(s)
                for param in stmt.params:
                    del self.vars[param]
        
        for stmt in program.stmts:
            self._check_stmt(stmt)
    
    def _check_stmt(self, stmt: A.Node) -> None:
        if isinstance(stmt, A.VarDecl):
            self._check_var_decl(stmt)
        elif isinstance(stmt, A.FuncDef):
            self._check_func_def(stmt)
        elif isinstance(stmt, A.Assign):
            self._check_assign(stmt)
        elif isinstance(stmt, A.IfStmt):
            self._check_if(stmt)
        elif isinstance(stmt, A.WhileStmt):
            self._check_while(stmt)
        elif isinstance(stmt, A.ReturnStmt):
            if stmt.value:
                self._check_expr(stmt.value)
    
    def _check_var_decl(self, decl: A.VarDecl) -> None:
        if decl.type_name:
            declared = parse_type(decl.type_name)
            self.vars[decl.name] = declared
        elif decl.value:
            val_type = self._check_expr(decl.value)
            if decl.type_name:
                declared = parse_type(decl.type_name)
                if not self._is_assignable(declared, val_type):
                    raise TypeCheckError(
                        f"Cannot assign {self._type_name(val_type)} to {decl.type_name}",
                        decl.line
                    )
            self.vars[decl.name] = val_type
    
    def _check_func_def(self, fn: A.FuncDef) -> None:
        for i, param in enumerate(fn.params):
            if i < len(fn.param_types):
                self.vars[param] = parse_type(fn.param_types[i])
            else:
                self.vars[param] = A.TAny()
        
        for stmt in fn.body:
            self._check_stmt(stmt)
        
        for param in fn.params:
            del self.vars[param]
    
    def _check_assign(self, assign: A.Assign) -> None:
        if isinstance(assign.target, A.Ident):
            if assign.target.name not in self.vars:
                raise TypeCheckError(f"Undefined variable '{assign.target.name}'", assign.line)
        
        if assign.value:
            self._check_expr(assign.value)
    
    def _check_if(self, if_stmt: A.IfStmt) -> None:
        cond_type = self._check_expr(if_stmt.condition)
        if not isinstance(cond_type, A.TBool) and not isinstance(cond_type, A.TAny):
            raise TypeCheckError("If condition must be boolean", if_stmt.line)
        
        for stmt in if_stmt.then_body:
            self._check_stmt(stmt)
        
        for elif_clause in if_stmt.elif_clauses:
            self._check_stmt(elif_clause)
        
        if if_stmt.else_body:
            for stmt in if_stmt.else_body:
                self._check_stmt(stmt)
    
    def _check_while(self, while_stmt: A.WhileStmt) -> None:
        cond_type = self._check_expr(while_stmt.condition)
        if not isinstance(cond_type, A.TBool) and not isinstance(cond_type, A.TAny):
            raise TypeCheckError("While condition must be boolean", while_stmt.line)
        
        for stmt in while_stmt.body:
            self._check_stmt(stmt)
    
    def _check_expr(self, expr: A.Node) -> A.Type:
        if isinstance(expr, A.IntLit):
            return A.TInt()
        if isinstance(expr, A.FloatLit):
            return A.TFloat()
        if isinstance(expr, A.StringLit):
            return A.TString()
        if isinstance(expr, A.BoolLit):
            return A.TBool()
        if isinstance(expr, A.NullLit):
            return A.TNull()
        if isinstance(expr, A.Ident):
            if expr.name not in self.vars:
                raise TypeCheckError(f"Undefined variable '{expr.name}'", expr.line)
            return self.vars[expr.name]
        if isinstance(expr, A.BinOp):
            return self._check_binop(expr)
        if isinstance(expr, A.UnaryOp):
            return self._check_unary(expr)
        if isinstance(expr, A.Call):
            return self._check_call(expr)
        if isinstance(expr, A.ListLit):
            return A.TList()
        if isinstance(expr, A.DictLit):
            return A.TDict()

        return A.TAny()
    
    def _check_binop(self, expr: A.BinOp) -> A.Type:
        left_type = self._check_expr(expr.left)
        right_type = self._check_expr(expr.right)
        
        if expr.op in ("+", "-", "*", "/", "%"):
            if isinstance(left_type, A.TInt) and isinstance(right_type, A.TInt):
                return A.TInt()
            if isinstance(left_type, A.TFloat) or isinstance(right_type, A.TFloat):
                return A.TFloat()
            if isinstance(left_type, A.TInt) or isinstance(right_type, A.TInt):
                return A.TFloat()
            return A.TAny()
        
        if expr.op in ("==", "!=", "<", "<=", ">", ">="):
            if self._is_assignable(left_type, right_type):
                return A.TBool()
            return A.TBool()
        
        if expr.op in ("&&", "||"):
            return A.TBool()
        
        return A.TAny()
    
    def _check_unary(self, expr: A.UnaryOp) -> A.Type:
        if expr.op == "-":
            val_type = self._check_expr(expr.operand)
            if isinstance(val_type, A.TInt):
                return A.TInt()
            return A.TFloat()
        if expr.op == "!":
            return A.TBool()
        return A.TAny()
    
    def _check_call(self, expr: A.Call) -> A.Type:
        if isinstance(expr.callee, A.Ident):
            fname = expr.callee.name
            if fname in self.funcs:
                param_types, ret_type = self.funcs[fname]
                if len(expr.args) != len(param_types):
                    raise TypeCheckError(
                        f"Function '{fname}' expects {len(param_types)} args, got {len(expr.args)}",
                        expr.line
                    )
                for i, arg in enumerate(expr.args):
                    self._check_expr(arg)
                return parse_type(ret_type) if ret_type else A.TAny()
        
        self._check_expr(expr.callee)
        for arg in expr.args:
            self._check_expr(arg)
        return A.TAny()
    
    def _is_assignable(self, target: A.Type, source: A.Type) -> bool:
        if isinstance(target, A.TAny) or isinstance(source, A.TAny):
            return True
        
        if isinstance(source, A.TInt) and isinstance(target, A.TFloat):
            return True
        
        return type(target) == type(source)
    
    def _type_name(self, t: A.Type) -> str:
        if isinstance(t, A.TInt):
            return "int"
        if isinstance(t, A.TFloat):
            return "float"
        if isinstance(t, A.TString):
            return "string"
        if isinstance(t, A.TBool):
            return "bool"
        if isinstance(t, A.TNull):
            return "null"
        if isinstance(t, A.TList):
            return "list"
        return "any"