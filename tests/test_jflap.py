"""Testa a linguagem lida dos .jff, sem interpretar rótulos como regex."""

from collections import defaultdict
import xml.etree.ElementTree as ET

import pytest

from src.automata import AFNe
from validate_afne_structure import ROOT
from validate_jflap_runtime import casos


@pytest.mark.parametrize("numero", range(1, 7))
def test_linguagem_dos_arquivos_jflap(numero):
    nome = f"ER-{numero:02}"
    automaton = ET.parse(ROOT / "docs/diagramas" / nome / f"{nome}.jff").getroot().find("automaton")
    estados = automaton.findall("state")
    iniciais = [s.get("id") for s in estados if s.find("initial") is not None]
    assert len(iniciais) == 1
    transicoes = defaultdict(set)
    alfabeto = set()
    for t in automaton.findall("transition"):
        simbolo = t.findtext("read") or ""
        assert len(simbolo) <= 1, f"Classe não expandida: {simbolo!r}"
        transicoes[(t.findtext("from"), simbolo)].add(t.findtext("to"))
        if simbolo:
            alfabeto.add(simbolo)
    afne = AFNe(
        {s.get("id") for s in estados}, alfabeto, transicoes, iniciais[0],
        {s.get("id") for s in estados if s.find("final") is not None},
    )
    for cadeia, esperado in casos(numero).items():
        assert afne.aceita(cadeia) == esperado, (nome, cadeia, esperado)
