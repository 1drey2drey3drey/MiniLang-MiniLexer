"""Testes estruturais dos seis AFNε e seus arquivos JFLAP."""

from __future__ import annotations

from validate_afne_structure import CANONICAS, validar_codigo, validar_jflap


def test_afne_python_matches_canonical_tables() -> None:
    for nome, spec in CANONICAS.items():
        assert validar_codigo(nome, spec) == [], f"Estrutura divergente em {nome}"


def test_jflap_matches_canonical_tables() -> None:
    for nome, spec in CANONICAS.items():
        assert validar_jflap(nome, spec) == [], f"JFLAP divergente em {nome}"
