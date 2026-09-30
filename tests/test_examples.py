from pathlib import Path

import pytest

from src.lexer import LexicalError, tokenize


ROOT = Path(__file__).resolve().parents[1]


def test_exemplo_valido_eh_tokenizado():
    source = (ROOT / "examples" / "valido.min").read_text(encoding="utf-8")
    tokens = tokenize(source)
    assert tokens
    assert tokens[0].lexeme == "program"
    assert tokens[-1].lexeme == "}"


def test_exemplo_invalido_dispara_erro_lexico():
    source = (ROOT / "examples" / "invalido.min").read_text(encoding="utf-8")
    with pytest.raises(LexicalError):
        tokenize(source)
