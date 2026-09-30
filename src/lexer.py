"""MiniLexer: análise léxica da MiniLang."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .patterns import (
    ASCII_LETTERS,
    ASCII_DIGITS,
    COMPILED,
    COMPOUND_OPERATORS,
    DELIMITERS,
    IDENTIFIER_CHARS,
    KEYWORDS,
    SIMPLE_OPERATORS,
    STRING_CHARACTERS,
    WHITESPACE,
)
from .tokens import Token, TokenType


@dataclass(frozen=True, slots=True)
class LexicalError(Exception):
    """Erro reportável pelo analisador léxico."""

    line: int
    column: int
    lexeme: str
    message: str

    def __str__(self) -> str:
        detalhe = f'Lexema: {self.lexeme!r}\n' if self.lexeme else ""
        return (
            "ERRO LÉXICO\n"
            f"Linha: {self.line}\n"
            f"Coluna: {self.column}\n"
            f"{detalhe}"
            f"Motivo: {self.message}"
        )


class MiniLexer:
    """Lexer baseado nas prioridades congeladas da especificação."""

    def __init__(self, source: str) -> None:
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1

    def lex(self) -> list[Token]:
        """Tokeniza a entrada inteira ou lança LexicalError."""
        if not self.source:
            return []

        tokens: list[Token] = []
        while self.pos < len(self.source):
            self._skip_whitespace()
            if self.pos >= len(self.source):
                break

            if self._starts_comment():
                self._skip_comment()
                continue

            token = self._next_token()
            tokens.append(token)

        return tokens

    def _next_token(self) -> Token:
        start_pos = self.pos
        start_line = self.line
        start_column = self.column
        char = self.source[self.pos]

        if char == '"':
            return self._scan_string(start_line, start_column)

        for lexeme, token_type in COMPOUND_OPERATORS.items():
            if self.source.startswith(lexeme, self.pos):
                self._advance_text(lexeme)
                return Token(token_type, lexeme, start_line, start_column)

        if char in ASCII_DIGITS:
            return self._scan_number_or_time(start_line, start_column)

        if char in ASCII_LETTERS:
            return self._scan_identifier(start_line, start_column)

        if char in SIMPLE_OPERATORS:
            self._advance_text(char)
            return Token(SIMPLE_OPERATORS[char], char, start_line, start_column)

        if char == "!":
            raise self._error("!", "o operador '!' isolado não é definido; use '!='")

        if char in DELIMITERS:
            self._advance_text(char)
            return Token(DELIMITERS[char], char, start_line, start_column)

        bad = self.source[start_pos : start_pos + 1]
        raise self._error(bad, "símbolo não reconhecido pela MiniLang")

    def _scan_string(self, line: int, column: int) -> Token:
        start = self.pos
        self._advance_text('"')

        while self.pos < len(self.source):
            char = self.source[self.pos]
            if char == '"':
                self._advance_text('"')
                lexeme = self.source[start : self.pos]
                return Token(TokenType.STRING, lexeme, line, column)
            if char not in STRING_CHARACTERS:
                trecho = self.source[start : min(len(self.source), self.pos + 1)]
                if char in "\r\n\t":
                    raise self._error(trecho, "string não pode conter tabulação ou quebra de linha")
                raise self._error(trecho, "caractere não permitido dentro da string")
            self._advance_text(char)

        lexeme = self.source[start : self.pos]
        raise self._error(lexeme, "string não encerrada", line, column)

    def _scan_number_or_time(self, line: int, column: int) -> Token:
        start = self.pos

        # TIME tem prioridade sobre INTEGER. Se houver a estrutura HH:MM,
        # verificamos a cadeia inteira para não aceitar 25:90 ou 14:30:00 por
        # fragmentação.
        time_match = re.match(r"[0-9]+:[0-9]+(?:[:][0-9]+)?", self.source[self.pos :])
        if time_match:
            candidate = time_match.group(0)
            match = COMPILED["ER-06"].fullmatch(candidate)
            if match:
                self._advance_text(candidate)
                return Token(TokenType.TIME, candidate, line, column)
            raise self._error(candidate, "formato de horário inválido; esperado HH:MM com HH=00–23 e MM=00–59", line, column)

        self._consume_digits()

        # Parte decimal.
        if self._peek() == ".":
            self._advance_text(".")
            self._consume_digits()

            # Um segundo ponto pertence ao mesmo candidato inválido, e não a
            # um possível próximo token.
            if self._peek() == ".":
                candidate = self._consume_numeric_continuation()
                raise self._error(self.source[start : self.pos], "formato numérico inválido", line, column)

        # Expoente científico opcional.
        if self._peek() in {"e", "E"}:
            self._advance_text(self._peek())
            if self._peek() in {"+", "-"}:
                self._advance_text(self._peek())
            self._consume_digits()

            candidate = self.source[start : self.pos]
            if not COMPILED["ER-04"].fullmatch(candidate):
                raise self._error(candidate, "notação científica inválida; o expoente deve possuir pelo menos um dígito", line, column)

            self._reject_numeric_contamination(start, line, column)
            return Token(TokenType.SCIENTIFIC, candidate, line, column)

        candidate = self.source[start : self.pos]

        # Se a candidata teve ponto, ela precisa ser um decimal válido.
        if "." in candidate:
            if not COMPILED["ER-03"].fullmatch(candidate):
                raise self._error(candidate, "número decimal inválido; a parte inteira não pode possuir zero à esquerda e deve haver dígitos após o ponto", line, column)
            self._reject_numeric_contamination(start, line, column)
            return Token(TokenType.DECIMAL, candidate, line, column)

        if not COMPILED["ER-02"].fullmatch(candidate):
            raise self._error(candidate, "inteiro inválido; zero à esquerda não é permitido", line, column)

        self._reject_numeric_contamination(start)
        return Token(TokenType.INTEGER, candidate, line, column)

    def _reject_numeric_contamination(
        self, start: int, line: int | None = None, column: int | None = None
    ) -> None:
        """Impede fragmentação de candidatos numéricos inválidos."""
        if self.pos >= len(self.source):
            return

        next_char = self.source[self.pos]
        if next_char in ASCII_LETTERS or next_char == "_":
            end = self.pos
            while end < len(self.source) and (
                self.source[end] in ASCII_LETTERS + ASCII_DIGITS
                or self.source[end] in "_."
            ):
                end += 1
            candidate = self.source[start:end]
            raise self._error(
                candidate,
                "lexema numérico contaminado por letra, sublinhado ou novo ponto",
                line,
                column,
            )
        if next_char == ".":
            end = self.pos
            while end < len(self.source) and (
                self.source[end] in ASCII_DIGITS or self.source[end] == "."
            ):
                end += 1
            candidate = self.source[start:end]
            raise self._error(candidate, "formato numérico inválido", line, column)

    def _consume_numeric_continuation(self) -> str:
        start = self.pos
        while self.pos < len(self.source) and (self.source[self.pos].isdigit() or self.source[self.pos] == "."):
            self._advance_text(self.source[self.pos])
        return self.source[start : self.pos]

    def _scan_identifier(self, line: int, column: int) -> Token:
        start = self.pos
        while self.pos < len(self.source) and self.source[self.pos] in IDENTIFIER_CHARS:
            self._advance_text(self.source[self.pos])

        candidate = self.source[start : self.pos]
        if not COMPILED["ER-01"].fullmatch(candidate):
            raise self._error(candidate, "identificador inválido: deve começar com letra, não pode terminar em '_' e não pode conter '__'", line, column)

        token_type = KEYWORDS.get(candidate, TokenType.IDENTIFIER)
        return Token(token_type, candidate, line, column)

    def _skip_whitespace(self) -> None:
        while self.pos < len(self.source) and self.source[self.pos] in WHITESPACE:
            self._advance_text(self.source[self.pos])

    def _starts_comment(self) -> bool:
        return self.source.startswith("//", self.pos)

    def _skip_comment(self) -> None:
        self._advance_text("//")
        while self.pos < len(self.source) and self.source[self.pos] not in "\r\n":
            self._advance_text(self.source[self.pos])

    def _peek(self) -> str:
        if self.pos >= len(self.source):
            return ""
        return self.source[self.pos]

    def _consume_digits(self) -> None:
        while self.pos < len(self.source) and self.source[self.pos] in ASCII_DIGITS:
            self._advance_text(self.source[self.pos])

    def _advance_text(self, text: str) -> None:
        if not self.source.startswith(text, self.pos):
            raise RuntimeError("avanço inconsistente do lexer")
        for char in text:
            self.pos += 1
            if char == "\n":
                self.line += 1
                self.column = 1
            else:
                self.column += 1

    def _error(
        self, lexeme: str, message: str, line: int | None = None, column: int | None = None
    ) -> LexicalError:
        return LexicalError(
            self.line if line is None else line,
            self.column if column is None else column,
            lexeme,
            message,
        )


def tokenize(source: str) -> list[Token]:
    """Função de conveniência para tokenizar uma entrada."""
    return MiniLexer(source).lex()


def format_tokens(tokens: list[Token]) -> str:
    """Formata a saída dos tokens para a demonstração."""
    if not tokens:
        return "Nenhum código foi fornecido.\n\nA análise léxica não foi realizada."
    return "\n".join(str(token) for token in tokens)
