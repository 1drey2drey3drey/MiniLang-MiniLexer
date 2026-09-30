"""Tipos e estruturas de tokens da MiniLang."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class TokenType(str, Enum):
    PROGRAM = "PROGRAM"

    TYPE_INT = "TYPE_INT"
    TYPE_FLOAT = "TYPE_FLOAT"
    TYPE_STRING = "TYPE_STRING"
    TYPE_BOOL = "TYPE_BOOL"
    TYPE_TIME = "TYPE_TIME"

    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    PRINT = "PRINT"
    BOOLEAN = "BOOLEAN"

    IDENTIFIER = "IDENTIFIER"

    INTEGER = "INTEGER"
    DECIMAL = "DECIMAL"
    SCIENTIFIC = "SCIENTIFIC"
    STRING = "STRING"
    TIME = "TIME"

    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"

    ASSIGN = "ASSIGN"
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    LESS = "LESS"
    GREATER = "GREATER"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER_EQUAL = "GREATER_EQUAL"

    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    SEMICOLON = "SEMICOLON"
    COMMA = "COMMA"


@dataclass(frozen=True, slots=True)
class Token:
    """Token reconhecido pelo lexer."""

    type: TokenType
    lexeme: str
    line: int
    column: int

    def __str__(self) -> str:
        # O lexema de STRING já contém as aspas da linguagem; não as duplicamos.
        exibicao = self.lexeme if self.type is TokenType.STRING else f'"{self.lexeme}"'
        return f'{self.type.value:<14} {exibicao} (linha {self.line}, coluna {self.column})'
