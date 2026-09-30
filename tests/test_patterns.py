import re

import pytest

from src.automata import (
    REGEX_ER01,
    REGEX_ER02,
    REGEX_ER03,
    REGEX_ER04,
    REGEX_ER05,
    REGEX_ER06,
    THOMPSON_COUNTS,
    construir_er01,
    construir_er02,
    construir_er03,
    construir_er04,
    construir_er05,
    construir_er06,
)


@pytest.mark.parametrize(
    ("nome", "construir", "regex"),
    [
        ("ER-01", construir_er01, REGEX_ER01),
        ("ER-02", construir_er02, REGEX_ER02),
        ("ER-03", construir_er03, REGEX_ER03),
        ("ER-04", construir_er04, REGEX_ER04),
        ("ER-05", construir_er05, REGEX_ER05),
        ("ER-06", construir_er06, REGEX_ER06),
    ],
)
def test_cada_regex_tem_afne(nome, construir, regex):
    afne = construir()
    assert len(afne.estados) == THOMPSON_COUNTS[nome]["estados"]
    assert afne.inicial == "q0"
    assert len(afne.finais) == 1


def comparar(afne, regex, casos):
    for cadeia in casos:
        esperado = re.fullmatch(regex, cadeia) is not None
        assert afne.aceita(cadeia) == esperado, cadeia


def test_er01_bateria():
    comparar(construir_er01(), REGEX_ER01, [
        "a", "nome", "idade", "aluno1", "valor_total", "a1_b2",
        "1aluno", "2idade", "_nome", "nome_", "nome__aluno", "nome__",
        "nome-aluno", "nome.aluno", "123", "",
    ])


def test_er02_bateria():
    comparar(construir_er02(), REGEX_ER02, [
        "0", "1", "7", "9", "10", "20", "2026", "999",
        "", "00", "01", "007", "0123", "-1", "1.5",
        "100", "09", "1a", "10a", "123.", "123_",
    ])


def test_er03_bateria():
    comparar(construir_er03(), REGEX_ER03, [
        "0.5", "0.50", "1.5", "9.5", "10.25", "2026.75",
        "00.5", "01.5", ".5", "5.", "1.2.3", "-9.5",
        "12.0", "100.001", "09.5",
    ])


def test_er04_bateria():
    comparar(construir_er04(), REGEX_ER04, [
        "1e3", "10e2", "0e5", "1.5e3", "9.5E-2", "10.25e+4",
        "", "1e", "1e+", ".5e2", "01e3", "1.5.2e3",
        "2E10", "0E-1", "12.0e+3", "9E2", "1.2E+10",
    ])


def test_er05_bateria():
    comparar(construir_er05(), REGEX_ER05, [
        '""', '"Andrey"', '"abc 123"', '"a_b.c"', '"hello!"', '"12:30"',
        "", '"abc', 'abc"', '"a"b"', '"a\\b"', '"linha\n', '"linha\t"',
    ])


def test_er06_bateria():
    comparar(construir_er06(), REGEX_ER06, [
        "00:00", "09:05", "12:30", "14:59", "23:00", "23:59",
        "24:00", "12:60", "2:30", "14:5", "99:99", "14:30:00",
    ])
