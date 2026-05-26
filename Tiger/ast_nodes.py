
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Any, Union



@dataclass(frozen=True)
class Type:
    pass

@dataclass(frozen=True)
class TInt(Type):
    pass

@dataclass(frozen=True)
class TFloat(Type):
    pass

@dataclass(frozen=True)
class TString(Type):
    pass

@dataclass(frozen=True)
class TBool(Type):
    pass

@dataclass(frozen=True)
class TNull(Type):
    pass

@dataclass(frozen=True)
class TVoid(Type):
    pass

@dataclass(frozen=True)
class TList(Type):
    elem_type: Type = field(default_factory=lambda: TFloat())

@dataclass(frozen=True)
class TDict(Type):
    pass

@dataclass(frozen=True)
class TAny(Type):
    pass

@dataclass(frozen=True)
class TFunction(Type):
    params: List[Type] = field(default_factory=list)
    ret_type: Type = field(default_factory=TVoid)



@dataclass
class Node:
    line: int = 0
    type: Optional[Type] = None  



@dataclass
class IntLit(Node):
    value: int = 0

@dataclass
class FloatLit(Node):
    value: float = 0.0

@dataclass
class StringLit(Node):
    value: str = ""

@dataclass
class BoolLit(Node):
    value: bool = False

@dataclass
class NullLit(Node):
    pass

@dataclass
class Ident(Node):
    name: str = ""

@dataclass
class BinOp(Node):
    op:    str = ""
    left:  Any = None
    right: Any = None

@dataclass
class UnaryOp(Node):
    op:      str = ""
    operand: Any = None

@dataclass
class Call(Node):
    callee: Any       = None
    args:   List[Any] = field(default_factory=list)

@dataclass
class MemberAccess(Node):
    obj:    Any = None
    member: str = ""

@dataclass
class Index(Node):
    obj:   Any = None
    index: Any = None

@dataclass
class ListLit(Node):
    elements: List[Any] = field(default_factory=list)

@dataclass
class DictLit(Node):
    keys: List[Any] = field(default_factory=list)
    values: List[Any] = field(default_factory=list)

@dataclass
class InputExpr(Node):
    prompt: Optional[Any] = None

@dataclass
class Assign(Node):
    target: Any = None
    op:     str = "="
    value:  Any = None



@dataclass
class VarDecl(Node):
    name: str = ""
    type_name: Optional[str] = None  
    value: Optional[Any] = None

@dataclass
class ExprStmt(Node):
    expr: Any = None

@dataclass
class PrintStmt(Node):
    args: List[Any] = field(default_factory=list)

@dataclass
class ReturnStmt(Node):
    value: Optional[Any] = None

@dataclass
class IfStmt(Node):
    condition:    Any            = None
    then_body:    List[Any]      = field(default_factory=list)
    elif_clauses: List[Any]      = field(default_factory=list)
    else_body:    Optional[List[Any]] = None

@dataclass
class ElifClause(Node):
    condition: Any       = None
    body:      List[Any] = field(default_factory=list)

@dataclass
class WhileStmt(Node):
    condition: Any       = None
    body:      List[Any] = field(default_factory=list)

@dataclass
class ForStmt(Node):
    var: str = ""
    iterable: Any = None
    body: List[Any] = field(default_factory=list)

@dataclass
class FuncDef(Node):
    name: str = ""
    params: List[str] = field(default_factory=list)
    param_types: List[str] = field(default_factory=list)  
    return_type: Optional[str] = None  
    body: List[Any] = field(default_factory=list)

@dataclass
class ImportStmt(Node):
    module: str = ""


@dataclass
class Program(Node):
    stmts: List[Any] = field(default_factory=list)
