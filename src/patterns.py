"""Padrões e tabelas utilizados pelo MiniLexer.

As seis ERs principais são exatamente as referências consolidadas no guia do
projeto. Comentários, palavras reservadas, operadores e delimitadores são
regras auxiliares do lexer.
"""

from __future__ import annotations

import re

from .automata import (
    REGEX_ER01,
    REGEX_ER02,
    REGEX_ER03,
    REGEX_ER04,
    REGEX_ER05,
    REGEX_ER06,
)
from .tokens import TokenType


REGEXES = {
    "ER-01": REGEX_ER01,
    "ER-02": REGEX_ER02,
    "ER-03": REGEX_ER03,
    "ER-04": REGEX_ER04,
    "ER-05": REGEX_ER05,
    "ER-06": REGEX_ER06,
}

COMPILED = {nome: re.compile(padrao) for nome, padrao in REGEXES.items()}

KEYWORDS: dict[str, TokenType] = {
    "program": TokenType.PROGRAM,
    "int": TokenType.TYPE_INT,
    "float": TokenType.TYPE_FLOAT,
    "string": TokenType.TYPE_STRING,
    "bool": TokenType.TYPE_BOOL,
    "time": TokenType.TYPE_TIME,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "print": TokenType.PRINT,
    "true": TokenType.BOOLEAN,
    "false": TokenType.BOOLEAN,
}

COMPOUND_OPERATORS: dict[str, TokenType] = {
    "==": TokenType.EQUAL,
    "!=": TokenType.NOT_EQUAL,
    "<=": TokenType.LESS_EQUAL,
    ">=": TokenType.GREATER_EQUAL,
}

SIMPLE_OPERATORS: dict[str, TokenType] = {
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.MULTIPLY,
    "/": TokenType.DIVIDE,
    "=": TokenType.ASSIGN,
    "<": TokenType.LESS,
    ">": TokenType.GREATER,
}

DELIMITERS: dict[str, TokenType] = {
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    "{": TokenType.LBRACE,
    "}": TokenType.RBRACE,
    ";": TokenType.SEMICOLON,
    ",": TokenType.COMMA,
}

ASCII_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
ASCII_DIGITS = "0123456789"

WHITESPACE = " \t\r\n"
STRING_CHARACTERS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 _.,!?;:+*/=<>-")
IDENTIFIER_CHARS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_")
