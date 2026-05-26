
from __future__ import annotations
from typing import List, Optional, Callable
from lexer import Lexer, Token, TT
import ast_nodes as A


class ParseError(Exception):
    def __init__(self, msg: str, token: Token):
        super().__init__(f"ParseError at line {token.line}, col {token.col}: {msg}")
        self.token = token



class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens  = tokens
        self.pos     = 0


    def _peek(self, offset: int = 0) -> Token:
        idx = self.pos + offset
        return self.tokens[idx] if idx < len(self.tokens) else self.tokens[-1]

    def _advance(self) -> Token:
        tok = self.tokens[self.pos]
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return tok

    def _check(self, *types: TT) -> bool:
        return self._peek().type in types

    def _match(self, *types: TT) -> Optional[Token]:
        if self._peek().type in types:
            return self._advance()
        return None

    def _expect(self, tt: TT, msg: str = "") -> Token:
        tok = self._peek()
        if tok.type != tt:
            raise ParseError(msg or f"Expected {tt.name}, got {tok.type.name} ({tok.value!r})", tok)
        return self._advance()

    def _skip_newlines(self):
        while self._check(TT.NEWLINE):
            self._advance()


    def parse(self) -> A.Program:
        stmts = []
        self._skip_newlines()
        while not self._check(TT.EOF):
            node = self._top_level()
            if node is not None:
                stmts.append(node)
            self._skip_newlines()
        return A.Program(stmts=stmts, line=1)

    def _top_level(self) -> Optional[A.Node]:
        if (self._peek(0).type == TT.IDENT and
                self._peek(1).type == TT.LPAREN and
                self._is_func_def()):
            return self._func_def()
        return self._stmt()

    def _is_func_def(self) -> bool:
        save = self.pos
        try:
            self._advance()   
            self._advance()   
            depth = 1
            while depth > 0:
                t = self._peek()
                if t.type == TT.EOF:
                    return False
                if t.type == TT.LPAREN:
                    depth += 1
                elif t.type == TT.RPAREN:
                    depth -= 1
                self._advance()
            while self._check(TT.NEWLINE):
                self._advance()
            if self._check(TT.COLON):
                self._advance()  
                while self._check(TT.NEWLINE):
                    self._advance()
                if self._check(TT.IDENT):
                    self._advance()  
                while self._check(TT.NEWLINE):
                    self._advance()
            return self._check(TT.LBRACE)
        finally:
            self.pos = save


    def _func_def(self) -> A.FuncDef:
        name_tok = self._expect(TT.IDENT)
        self._expect(TT.LPAREN)
        params, param_types = self._param_list()
        self._expect(TT.RPAREN)
        
        return_type = None
        if self._check(TT.COLON):
            self._advance()
            if self._check(TT.IDENT):
                return_type = self._advance().value
        
        self._skip_newlines()
        body = self._block()
        return A.FuncDef(name=name_tok.value, params=params, param_types=param_types,
                        return_type=return_type, body=body, line=name_tok.line)

    def _param_list(self) -> tuple:
        params = []
        param_types = []
        if self._check(TT.RPAREN):
            return params, param_types
        
        name_tok = self._expect(TT.IDENT, "Expected parameter name")
        params.append(name_tok.value)
        
        ptype = None
        if self._check(TT.COLON):
            self._advance()
            if self._check(TT.IDENT):
                ptype = self._advance().value
        param_types.append(ptype)
        
        while self._match(TT.COMMA):
            name_tok = self._expect(TT.IDENT, "Expected parameter name")
            params.append(name_tok.value)
            
            ptype = None
            if self._check(TT.COLON):
                self._advance()
                if self._check(TT.IDENT):
                    ptype = self._advance().value
            param_types.append(ptype)
        
        return params, param_types

    def _block(self) -> List[A.Node]:
        self._expect(TT.LBRACE)
        self._skip_newlines()
        stmts = []
        while not self._check(TT.RBRACE) and not self._check(TT.EOF):
            s = self._stmt()
            if s is not None:
                stmts.append(s)
            self._skip_newlines()
        self._expect(TT.RBRACE)
        return stmts


    def _stmt(self) -> Optional[A.Node]:
        self._skip_newlines()
        tok = self._peek()

        if tok.type == TT.NEWLINE:
            self._advance()
            return None

        if tok.type == TT.VAR:
            return self._var_decl()
        if tok.type == TT.IF:
            return self._if_stmt()
        if tok.type == TT.WHILE:
            return self._while_stmt()
        if tok.type == TT.FOR:
            return self._for_stmt()
        if tok.type == TT.RETURN:
            return self._return_stmt()
        if tok.type == TT.PRINT:
            return self._print_stmt()
        if tok.type == TT.IMPORT:
            return self._import_stmt()
        if tok.type == TT.EOF:
            return None

        return self._assign_or_expr_stmt()

    def _var_decl(self) -> A.VarDecl:
        tok = self._expect(TT.VAR)
        name = self._expect(TT.IDENT, "Expected variable name after 'var'").value
        
        type_name = None
        if self._check(TT.COLON):
            self._advance()
            if self._check(TT.IDENT):
                type_name = self._advance().value
        
        value = None
        if self._match(TT.ASSIGN):
            value = self._expr()
        self._stmt_end()
        return A.VarDecl(name=name, type_name=type_name, value=value, line=tok.line)

    def _if_stmt(self) -> A.IfStmt:
        tok = self._expect(TT.IF)
        cond = self._expr()
        if self._check(TT.RPAREN):
            self._advance()  
        self._skip_newlines()
        then_body = self._block()

        elif_clauses = []
        else_body    = None

        while True:
            self._skip_newlines()
            if self._check(TT.ELIF):
                et = self._advance()
                ec = self._expr()
                if self._check(TT.RPAREN):
                    self._advance()
                self._skip_newlines()
                eb = self._block()
                elif_clauses.append(A.ElifClause(condition=ec, body=eb, line=et.line))
            elif self._check(TT.ELSE):
                self._advance()
                self._skip_newlines()
                else_body = self._block()
                break
            else:
                break

        return A.IfStmt(condition=cond, then_body=then_body,
                        elif_clauses=elif_clauses, else_body=else_body, line=tok.line)

    def _while_stmt(self) -> A.WhileStmt:
        tok = self._expect(TT.WHILE)
        cond = self._expr()
        if self._check(TT.RPAREN):
            self._advance()
        self._skip_newlines()
        body = self._block()
        return A.WhileStmt(condition=cond, body=body, line=tok.line)

    def _for_stmt(self) -> A.ForStmt:
        tok = self._expect(TT.FOR)
        var_name = self._expect(TT.IDENT, "Expected loop variable name").value
        self._expect(TT.IN, "Expected 'in' in for loop")
        iterable = self._expr()
        if self._check(TT.RPAREN):
            self._advance()
        self._skip_newlines()
        body = self._block()
        return A.ForStmt(var=var_name, iterable=iterable, body=body, line=tok.line)

    def _return_stmt(self) -> A.ReturnStmt:
        tok = self._expect(TT.RETURN)
        value = None
        if not self._check(TT.NEWLINE) and not self._check(TT.EOF):
            value = self._expr()
        self._stmt_end()
        return A.ReturnStmt(value=value, line=tok.line)

    def _print_stmt(self) -> A.PrintStmt:
        tok = self._expect(TT.PRINT)
        self._expect(TT.LPAREN, "Expected '(' after 'print'")
        args = []
        if not self._check(TT.RPAREN):
            args.append(self._expr())
            while self._match(TT.COMMA):
                args.append(self._expr())
        self._expect(TT.RPAREN, "Expected ')' to close print()")
        self._stmt_end()
        return A.PrintStmt(args=args, line=tok.line)

    def _import_stmt(self) -> A.ImportStmt:
        tok = self._expect(TT.IMPORT)
        name = self._expect(TT.IDENT, "Expected module name after 'import'").value
        self._stmt_end()
        return A.ImportStmt(module=name, line=tok.line)

    def _assign_or_expr_stmt(self) -> A.Node:
        line = self._peek().line
        left = self._expr()

        assign_ops = {TT.ASSIGN, TT.PLUS_EQ, TT.MINUS_EQ, TT.STAR_EQ, TT.SLASH_EQ}
        if self._peek().type in assign_ops:
            op_tok = self._advance()
            right  = self._expr()
            self._stmt_end()
            node = A.Assign(target=left, op=op_tok.value, value=right, line=line)
            return node

        self._stmt_end()
        return A.ExprStmt(expr=left, line=line)

    def _stmt_end(self):
        if self._check(TT.NEWLINE):
            self._advance()
        elif self._check(TT.EOF) or self._check(TT.RBRACE):
            pass


    def _expr(self) -> A.Node:
        return self._or_expr()

    def _or_expr(self) -> A.Node:
        left = self._and_expr()
        while self._check(TT.OR):
            op = self._advance()
            right = self._and_expr()
            left = A.BinOp(op="||", left=left, right=right, line=op.line)
        return left

    def _and_expr(self) -> A.Node:
        left = self._not_expr()
        while self._check(TT.AND):
            op = self._advance()
            right = self._not_expr()
            left = A.BinOp(op="&&", left=left, right=right, line=op.line)
        return left

    def _not_expr(self) -> A.Node:
        if self._check(TT.NOT):
            op = self._advance()
            return A.UnaryOp(op="!", operand=self._not_expr(), line=op.line)
        return self._comparison()

    def _comparison(self) -> A.Node:
        cmp_ops = {TT.EQ: "==", TT.NEQ: "!=", TT.LT: "<",
                   TT.LE: "<=", TT.GT: ">", TT.GE: ">="}
        left = self._additive()
        while self._peek().type in cmp_ops:
            op_tok = self._advance()
            right  = self._additive()
            left   = A.BinOp(op=cmp_ops[op_tok.type], left=left,
                              right=right, line=op_tok.line)
        return left

    def _additive(self) -> A.Node:
        left = self._multiplicative()
        while self._check(TT.PLUS, TT.MINUS):
            op_tok = self._advance()
            right  = self._multiplicative()
            left   = A.BinOp(op=op_tok.value, left=left, right=right, line=op_tok.line)
        return left

    def _multiplicative(self) -> A.Node:
        left = self._unary()
        while self._check(TT.STAR, TT.SLASH, TT.PERCENT):
            op_tok = self._advance()
            right  = self._unary()
            left   = A.BinOp(op=op_tok.value, left=left, right=right, line=op_tok.line)
        return left

    def _unary(self) -> A.Node:
        if self._check(TT.MINUS):
            op = self._advance()
            return A.UnaryOp(op="-", operand=self._unary(), line=op.line)
        return self._postfix()

    def _postfix(self) -> A.Node:
        expr = self._primary()
        while True:
            if self._check(TT.DOT):
                self._advance()
                member = self._expect(TT.IDENT, "Expected member name after '.'")
                if self._check(TT.LPAREN):
                    self._advance()
                    args = self._arg_list()
                    self._expect(TT.RPAREN, "Expected ')' to close method call")
                    callee = A.MemberAccess(obj=expr, member=member.value, line=member.line)
                    expr   = A.Call(callee=callee, args=args, line=member.line)
                else:
                    expr = A.MemberAccess(obj=expr, member=member.value, line=member.line)
            elif self._check(TT.LBRACKET):
                self._advance()
                idx = self._expr()
                self._expect(TT.RBRACKET, "Expected ']'")
                expr = A.Index(obj=expr, index=idx, line=expr.line)
            elif self._check(TT.LPAREN):
                self._advance()
                args = self._arg_list()
                self._expect(TT.RPAREN, "Expected ')' to close call")
                expr = A.Call(callee=expr, args=args, line=expr.line)
            else:
                break
        return expr

    def _arg_list(self) -> List[A.Node]:
        args = []
        if self._check(TT.RPAREN):
            return args
        args.append(self._expr())
        while self._match(TT.COMMA):
            args.append(self._expr())
        return args

    def _primary(self) -> A.Node:
        tok = self._peek()

        if tok.type == TT.INT:
            self._advance()
            return A.IntLit(value=tok.value, line=tok.line)
        if tok.type == TT.FLOAT:
            self._advance()
            return A.FloatLit(value=tok.value, line=tok.line)
        if tok.type == TT.STRING:
            self._advance()
            return A.StringLit(value=tok.value, line=tok.line)
        if tok.type == TT.BOOL:
            self._advance()
            return A.BoolLit(value=tok.value, line=tok.line)
        if tok.type == TT.NULL:
            self._advance()
            return A.NullLit(line=tok.line)
        if tok.type == TT.IDENT:
            self._advance()
            return A.Ident(name=tok.value, line=tok.line)
        if tok.type == TT.INPUT:
            return self._input_expr()
        if tok.type == TT.LPAREN:
            self._advance()
            inner = self._expr()
            self._expect(TT.RPAREN, "Expected ')'")
            return inner
        if tok.type == TT.LBRACKET:
            return self._list_lit()
        if tok.type == TT.LBRACE:
            return self._dict_lit()

        raise ParseError(f"Unexpected token {tok.type.name} ({tok.value!r}) in expression", tok)

    def _input_expr(self) -> A.InputExpr:
        tok = self._expect(TT.INPUT)
        prompt = None
        if self._check(TT.LPAREN):
            self._advance()
            if not self._check(TT.RPAREN):
                prompt = self._expr()
            self._expect(TT.RPAREN, "Expected ')' to close input()")
        return A.InputExpr(prompt=prompt, line=tok.line)

    def _list_lit(self) -> A.ListLit:
        tok = self._expect(TT.LBRACKET)
        elements = []
        if not self._check(TT.RBRACKET):
            elements.append(self._expr())
            while self._match(TT.COMMA):
                if self._check(TT.RBRACKET):
                    break
                elements.append(self._expr())
        self._expect(TT.RBRACKET, "Expected ']'")
        return A.ListLit(elements=elements, line=tok.line)

    def _dict_lit(self) -> A.DictLit:
        tok = self._expect(TT.LBRACE)
        keys = []
        values = []
        self._skip_newlines()
        if not self._check(TT.RBRACE):
            while True:
                key = self._expr()
                self._expect(TT.COLON, "Expected ':' after dictionary key")
                value = self._expr()
                keys.append(key)
                values.append(value)
                self._skip_newlines()
                if not self._match(TT.COMMA):
                    break
                self._skip_newlines()
        self._expect(TT.RBRACE, "Expected '}'")
        return A.DictLit(keys=keys, values=values, line=tok.line)



def parse_source(source: str) -> A.Program:
    lexer  = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()
