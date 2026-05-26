
from __future__ import annotations
import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import List


class TT(Enum):
    INT        = auto()
    FLOAT      = auto()
    STRING     = auto()
    BOOL       = auto()
    NULL       = auto()

    IDENT      = auto()
    VAR        = auto()
    IF         = auto()
    ELIF       = auto()
    ELSE       = auto()
    WHILE      = auto()
    FOR        = auto()
    IN         = auto()
    RETURN     = auto()
    PRINT      = auto()
    INPUT      = auto()
    IMPORT     = auto()
    AND        = auto()
    OR         = auto()
    NOT        = auto()

    PLUS       = auto()
    MINUS      = auto()
    STAR       = auto()
    SLASH      = auto()
    PERCENT    = auto()
    EQ         = auto()   
    NEQ        = auto()   
    LT         = auto()
    LE         = auto()
    GT         = auto()
    GE         = auto()
    ASSIGN     = auto()   
    PLUS_EQ    = auto()   
    MINUS_EQ   = auto()   
    STAR_EQ    = auto()   
    SLASH_EQ   = auto()   

    LPAREN     = auto()
    RPAREN     = auto()
    LBRACE     = auto()
    RBRACE     = auto()
    LBRACKET   = auto()
    RBRACKET   = auto()
    COMMA      = auto()
    DOT        = auto()
    COLON      = auto()
    NEWLINE    = auto()

    EOF        = auto()


KEYWORDS: dict[str, TT] = {
    "var":    TT.VAR,
    "if":     TT.IF,
    "elif":   TT.ELIF,
    "else":   TT.ELSE,
    "while":  TT.WHILE,
    "for":    TT.FOR,
    "in":     TT.IN,
    "return": TT.RETURN,
    "print":  TT.PRINT,
    "input":  TT.INPUT,
    "import": TT.IMPORT,
    "and":    TT.AND,
    "or":     TT.OR,
    "not":    TT.NOT,
    "true":   TT.BOOL,
    "false":  TT.BOOL,
    "null":   TT.NULL,
}


@dataclass
class Token:
    type:   TT
    value:  object
    line:   int
    col:    int

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, L{self.line}:C{self.col})"


class LexerError(Exception):
    def __init__(self, msg: str, line: int, col: int):
        super().__init__(f"LexerError at line {line}, col {col}: {msg}")
        self.line = line
        self.col  = col


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos    = 0
        self.line   = 1
        self.col    = 1
        self.tokens: List[Token] = []


    def _peek(self, offset: int = 0) -> str:
        idx = self.pos + offset
        return self.source[idx] if idx < len(self.source) else "\0"

    def _advance(self) -> str:
        ch = self.source[self.pos]
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.col   = 1
        else:
            self.col += 1
        return ch

    def _match(self, expected: str) -> bool:
        if self._peek() == expected:
            self._advance()
            return True
        return False

    def _add(self, tt: TT, value: object = None, line: int = None, col: int = None):
        self.tokens.append(Token(tt, value, line or self.line, col or self.col))


    def tokenize(self) -> List[Token]:
        while self.pos < len(self.source):
            self._scan_token()

        self._add(TT.EOF, None)
        return self.tokens

    def _scan_token(self):
        line, col = self.line, self.col
        ch = self._advance()

        if ch in (" ", "\t", "\r"):
            return

        if ch == "\n":
            if self.tokens and self.tokens[-1].type != TT.NEWLINE:
                self._add(TT.NEWLINE, "\n", line, col)
            return

        if ch == "#":
            while self._peek() not in ("\n", "\0"):
                self._advance()
            return

        if ch in ('"', "'"):
            self._string(ch, line, col)
            return

        if ch.isdigit():
            self._number(ch, line, col)
            return

        if ch.isalpha() or ch == "_":
            self._ident(ch, line, col)
            return

        simple = {
            "(": TT.LPAREN, ")": TT.RPAREN,
            "{": TT.LBRACE, "}": TT.RBRACE,
            "[": TT.LBRACKET, "]": TT.RBRACKET,
            ",": TT.COMMA,   ".": TT.DOT,
            ":": TT.COLON,   "%": TT.PERCENT,
        }
        if ch in simple:
            self._add(simple[ch], ch, line, col)
            return

        if ch == "+":
            if self._match("="):
                self._add(TT.PLUS_EQ, "+=", line, col)
            else:
                self._add(TT.PLUS, "+", line, col)
            return
        if ch == "-":
            if self._match("="):
                self._add(TT.MINUS_EQ, "-=", line, col)
            else:
                self._add(TT.MINUS, "-", line, col)
            return
        if ch == "*":
            if self._match("="):
                self._add(TT.STAR_EQ, "*=", line, col)
            else:
                self._add(TT.STAR, "*", line, col)
            return
        if ch == "/":
            if self._match("/"):            
                while self._peek() not in ("\n", "\0"):
                    self._advance()
                return
            if self._match("="):
                self._add(TT.SLASH_EQ, "/=", line, col)
            else:
                self._add(TT.SLASH, "/", line, col)
            return
        if ch == "=":
            if self._match("="):
                self._add(TT.EQ, "==", line, col)
            else:
                self._add(TT.ASSIGN, "=", line, col)
            return
        if ch == "!":
            if self._match("="):
                self._add(TT.NEQ, "!=", line, col)
            else:
                raise LexerError(f"Unexpected character '!'", line, col)
            return
        if ch == "<":
            if self._match("="):
                self._add(TT.LE, "<=", line, col)
            else:
                self._add(TT.LT, "<", line, col)
            return
        if ch == ">":
            if self._match("="):
                self._add(TT.GE, ">=", line, col)
            else:
                self._add(TT.GT, ">", line, col)
            return

        raise LexerError(f"Unexpected character {ch!r}", line, col)


    def _string(self, quote: str, line: int, col: int):
        buf = []
        while True:
            ch = self._peek()
            if ch == "\0":
                raise LexerError("Unterminated string literal", line, col)
            if ch == "\n":
                raise LexerError("Newline inside string literal", line, col)
            if ch == "\\":
                self._advance()
                esc = self._advance()
                mapping = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\",
                           "'": "'",  '"': '"'}
                buf.append(mapping.get(esc, esc))
                continue
            if ch == quote:
                self._advance()
                break
            buf.append(self._advance())
        self._add(TT.STRING, "".join(buf), line, col)

    def _number(self, first: str, line: int, col: int):
        buf = [first]
        is_float = False
        while self._peek().isdigit():
            buf.append(self._advance())
        if self._peek() == "." and self._peek(1).isdigit():
            is_float = True
            buf.append(self._advance())   
            while self._peek().isdigit():
                buf.append(self._advance())
        raw = "".join(buf)
        self._add(TT.FLOAT if is_float else TT.INT,
                  float(raw) if is_float else int(raw), line, col)

    def _ident(self, first: str, line: int, col: int):
        buf = [first]
        while self._peek().isalnum() or self._peek() == "_":
            buf.append(self._advance())
        name = "".join(buf)
        tt = KEYWORDS.get(name, TT.IDENT)
        value = name
        if tt == TT.BOOL:
            value = True if name == "true" else False
        elif tt == TT.NULL:
            value = None
        self._add(tt, value, line, col)
