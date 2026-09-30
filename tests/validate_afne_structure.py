"""Validação estrutural exata dos seis AFNε da MiniLang.

A referência deste arquivo é a tabela canônica registrada no
MiniLang_Guia_Projeto.md. A validação compara:

1. Q, estado inicial e estado final;
2. todas as transições do AFNε implementado em Python, após expansão das
   classes agrupadas;
3. contagem canônica de Thompson (estados/transições/ε/rotuladas);
4. estrutura e rótulos dos seis arquivos JFLAP (.jff).

A validação é estrutural: uma máquina que apenas reconheça a mesma linguagem,
mas tenha uma tabela de transições diferente, deve falhar aqui.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.automata import (  # noqa: E402
    EPSILON,
    THOMPSON_COUNTS,
    construir_er01,
    construir_er02,
    construir_er03,
    construir_er04,
    construir_er05,
    construir_er06,
)


# Tabelas canônicas transcritas da especificação consolidada.
CANONICAS = {
    "ER-01": {
        "estados": 28,
        "inicial": "q0",
        "final": "q27",
        "classes": {
            "L": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
            "D": "0123456789",
        },
        "transicoes": [
            ("q0", "L", "q1"),
            ("q1", EPSILON, "q26"),
            ("q6", EPSILON, "q2"),
            ("q6", EPSILON, "q4"),
            ("q2", "L", "q3"),
            ("q3", EPSILON, "q7"),
            ("q4", "D", "q5"),
            ("q5", EPSILON, "q7"),
            ("q8", "_", "q9"),
            ("q9", EPSILON, "q14"),
            ("q14", EPSILON, "q10"),
            ("q14", EPSILON, "q12"),
            ("q10", "L", "q11"),
            ("q11", EPSILON, "q15"),
            ("q12", "D", "q13"),
            ("q13", EPSILON, "q15"),
            ("q15", EPSILON, "q16"),
            ("q16", EPSILON, "q18"),
            ("q16", EPSILON, "q17"),
            ("q18", EPSILON, "q20"),
            ("q18", EPSILON, "q22"),
            ("q20", "L", "q21"),
            ("q22", "D", "q23"),
            ("q21", EPSILON, "q19"),
            ("q23", EPSILON, "q19"),
            ("q19", EPSILON, "q18"),
            ("q19", EPSILON, "q17"),
            ("q24", EPSILON, "q6"),
            ("q24", EPSILON, "q8"),
            ("q7", EPSILON, "q25"),
            ("q17", EPSILON, "q25"),
            ("q26", EPSILON, "q24"),
            ("q26", EPSILON, "q27"),
            ("q25", EPSILON, "q24"),
            ("q25", EPSILON, "q27"),
        ],
    },
    "ER-02": {
        "estados": 10,
        "inicial": "q0",
        "final": "q1",
        "classes": {"N": "123456789", "D": "0123456789"},
        "transicoes": [
            ("q0", EPSILON, "q2"),
            ("q0", EPSILON, "q4"),
            ("q2", "0", "q3"),
            ("q3", EPSILON, "q1"),
            ("q4", "N", "q5"),
            ("q5", EPSILON, "q8"),
            ("q8", EPSILON, "q6"),
            ("q8", EPSILON, "q9"),
            ("q6", "D", "q7"),
            ("q7", EPSILON, "q6"),
            ("q7", EPSILON, "q9"),
            ("q9", EPSILON, "q1"),
        ],
    },
    "ER-03": {
        "estados": 18,
        "inicial": "q0",
        "final": "q17",
        "classes": {"N": "123456789", "D": "0123456789", "P": "."},
        "transicoes": [
            ("q2", "0", "q3"),
            ("q0", EPSILON, "q2"),
            ("q3", EPSILON, "q1"),
            ("q4", "N", "q5"),
            ("q8", "D", "q9"),
            ("q6", EPSILON, "q8"),
            ("q6", EPSILON, "q7"),
            ("q9", EPSILON, "q8"),
            ("q9", EPSILON, "q7"),
            ("q5", EPSILON, "q6"),
            ("q0", EPSILON, "q4"),
            ("q7", EPSILON, "q1"),
            ("q10", "P", "q11"),
            ("q1", EPSILON, "q10"),
            ("q12", "D", "q13"),
            ("q11", EPSILON, "q12"),
            ("q16", "D", "q17"),
            ("q14", EPSILON, "q16"),
            ("q14", EPSILON, "q17"),
            ("q17", EPSILON, "q16"),
            ("q17", EPSILON, "q15"),
            ("q13", EPSILON, "q14"),
        ],
    },
    "ER-04": {
        "estados": 42,
        "inicial": "q0",
        "final": "q39",
        "classes": {"N": "123456789", "D": "0123456789", "P": "."},
        "transicoes": [
            ("q2", "0", "q3"),
            ("q0", EPSILON, "q2"),
            ("q3", EPSILON, "q1"),
            ("q4", "N", "q5"),
            ("q8", "D", "q9"),
            ("q6", EPSILON, "q8"),
            ("q6", EPSILON, "q7"),
            ("q9", EPSILON, "q8"),
            ("q9", EPSILON, "q7"),
            ("q5", EPSILON, "q6"),
            ("q0", EPSILON, "q4"),
            ("q7", EPSILON, "q1"),
            ("q12", "P", "q13"),
            ("q14", "D", "q15"),
            ("q13", EPSILON, "q14"),
            ("q18", "D", "q19"),
            ("q16", EPSILON, "q18"),
            ("q16", EPSILON, "q17"),
            ("q19", EPSILON, "q18"),
            ("q19", EPSILON, "q17"),
            ("q15", EPSILON, "q16"),
            ("q10", EPSILON, "q12"),
            ("q17", EPSILON, "q11"),
            ("q20", EPSILON, "q21"),
            ("q10", EPSILON, "q20"),
            ("q21", EPSILON, "q11"),
            ("q1", EPSILON, "q10"),
            ("q24", "e", "q25"),
            ("q22", EPSILON, "q24"),
            ("q25", EPSILON, "q23"),
            ("q26", "E", "q27"),
            ("q22", EPSILON, "q26"),
            ("q27", EPSILON, "q23"),
            ("q11", EPSILON, "q22"),
            ("q30", "+", "q31"),
            ("q28", EPSILON, "q30"),
            ("q31", EPSILON, "q29"),
            ("q32", "-", "q33"),
            ("q28", EPSILON, "q32"),
            ("q33", EPSILON, "q29"),
            ("q34", EPSILON, "q35"),
            ("q28", EPSILON, "q34"),
            ("q35", EPSILON, "q29"),
            ("q23", EPSILON, "q28"),
            ("q36", "D", "q37"),
            ("q29", EPSILON, "q36"),
            ("q40", "D", "q41"),
            ("q38", EPSILON, "q40"),
            ("q38", EPSILON, "q39"),
            ("q41", EPSILON, "q40"),
            ("q41", EPSILON, "q39"),
            ("q37", EPSILON, "q38"),
        ],
    },
    "ER-05": {
        "estados": 8,
        "inicial": "q0",
        "final": "q7",
        "classes": {
            "C": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 _.,!?;:+*/=<>-"
        },
        "transicoes": [
            ("q0", '"', "q1"),
            ("q4", "C", "q5"),
            ("q2", EPSILON, "q4"),
            ("q2", EPSILON, "q3"),
            ("q5", EPSILON, "q4"),
            ("q5", EPSILON, "q3"),
            ("q1", EPSILON, "q2"),
            ("q6", '"', "q7"),
            ("q3", EPSILON, "q6"),
        ],
    },
    "ER-06": {
        "estados": 16,
        "inicial": "q0",
        "final": "q15",
        "classes": {"01": "01", "0123": "0123", "012345": "012345", "D": "0123456789"},
        "transicoes": [
            ("q2", "01", "q3"),
            ("q4", "D", "q5"),
            ("q3", EPSILON, "q4"),
            ("q0", EPSILON, "q2"),
            ("q5", EPSILON, "q1"),
            ("q6", "2", "q7"),
            ("q8", "0123", "q9"),
            ("q7", EPSILON, "q8"),
            ("q0", EPSILON, "q6"),
            ("q9", EPSILON, "q1"),
            ("q10", ":", "q11"),
            ("q1", EPSILON, "q10"),
            ("q12", "012345", "q13"),
            ("q14", "D", "q15"),
            ("q13", EPSILON, "q14"),
            ("q11", EPSILON, "q12"),
        ],
    },
}

CONSTRUTORES = {
    "ER-01": construir_er01,
    "ER-02": construir_er02,
    "ER-03": construir_er03,
    "ER-04": construir_er04,
    "ER-05": construir_er05,
    "ER-06": construir_er06,
}

# Rótulos explícitos reconhecidos pelo JFLAP para conjuntos finitos.
JFLAP_LABELS = {
    "L": "[A-Za-z]",
    "D": "[0-9]",
    "N": "[1-9]",
    "P": ".",
    "C": "[A-Za-z0-9 _.,!?;:+*/=<>-]",
    "01": "[01]",
    "0123": "[0-3]",
    "012345": "[0-5]",
}


def _expand_expected(spec: dict) -> tuple[set[str], dict[tuple[str, str], frozenset[str]]]:
    alphabet: set[str] = set()
    expanded: dict[tuple[str, str], set[str]] = defaultdict(set)

    for origem, rotulo, destino in spec["transicoes"]:
        if rotulo == EPSILON:
            expanded[(origem, EPSILON)].add(destino)
            continue
        simbolos = spec["classes"].get(rotulo, rotulo)
        for simbolo in simbolos:
            expanded[(origem, simbolo)].add(destino)
            alphabet.add(simbolo)

    return alphabet, {chave: frozenset(destinos) for chave, destinos in expanded.items()}


def validar_codigo(nome: str, spec: dict) -> list[str]:
    erros: list[str] = []
    afne = CONSTRUTORES[nome]()
    esperados_estados = {f"q{i}" for i in range(spec["estados"])}
    esperado_alfabeto, esperado_transicoes = _expand_expected(spec)

    if afne.estados != frozenset(esperados_estados):
        erros.append(f"estados: esperado {len(esperados_estados)}, obtido {len(afne.estados)}")

    if afne.inicial != spec["inicial"]:
        erros.append(f"inicial: esperado {spec['inicial']}, obtido {afne.inicial}")

    finais_esperados = frozenset({spec["final"]})
    if afne.finais != finais_esperados:
        erros.append(f"finais: esperado {sorted(finais_esperados)}, obtido {sorted(afne.finais)}")

    if afne.alfabeto != frozenset(esperado_alfabeto):
        extras = sorted(afne.alfabeto - frozenset(esperado_alfabeto))
        faltantes = sorted(frozenset(esperado_alfabeto) - afne.alfabeto)
        erros.append(f"alfabeto: extras={extras}, faltantes={faltantes}")

    if afne.transicoes != esperado_transicoes:
        chaves = set(afne.transicoes) | set(esperado_transicoes)
        diferencas = []
        for chave in sorted(chaves):
            obtido = afne.transicoes.get(chave, frozenset())
            esperado = esperado_transicoes.get(chave, frozenset())
            if obtido != esperado:
                diferencas.append((chave, sorted(esperado), sorted(obtido)))
        erros.append(f"transições divergentes: {diferencas[:5]}")

    c = THOMPSON_COUNTS[nome]
    total = len(spec["transicoes"])
    epsilon = sum(1 for _, simbolo, _ in spec["transicoes"] if simbolo == EPSILON)
    rotuladas = total - epsilon
    if c["estados"] != spec["estados"] or c["transicoes"] != total or c["epsilon"] != epsilon or c["rotuladas"] != rotuladas:
        erros.append(
            "THOMPSON_COUNTS inconsistente com tabela canônica: "
            f"esperado {spec['estados']}/{total}/{epsilon}/{rotuladas}, obtido {c}"
        )

    return erros


def validar_jflap(nome: str, spec: dict) -> list[str]:
    erros: list[str] = []
    caminho = ROOT / "docs" / "diagramas" / nome / f"{nome}.jff"
    if not caminho.exists():
        return [f"arquivo ausente: {caminho}"]

    try:
        tree = ET.parse(caminho)
    except ET.ParseError as exc:
        return [f"XML inválido: {exc}"]

    root = tree.getroot()
    automaton = root.find("automaton")
    if automaton is None:
        return ["elemento <automaton> ausente"]

    states = automaton.findall("state")
    expected_names = {f"q{i}" for i in range(spec["estados"])}
    actual_names = {state.get("name") for state in states}
    if actual_names != expected_names:
        erros.append("estados JFLAP divergentes")

    initial = {state.get("name") for state in states if state.find("initial") is not None}
    finals = {state.get("name") for state in states if state.find("final") is not None}
    if initial != {spec["inicial"]}:
        erros.append(f"inicial JFLAP: esperado {{{spec['inicial']}}}, obtido {sorted(initial)}")
    if finals != {spec["final"]}:
        erros.append(f"final JFLAP: esperado {{{spec['final']}}}, obtido {sorted(finals)}")

    ids_to_names = {state.get("id"): state.get("name") for state in states}
    atual = []
    for transition in automaton.findall("transition"):
        origem = ids_to_names.get(transition.findtext("from"))
        destino = ids_to_names.get(transition.findtext("to"))
        leitura = transition.findtext("read") or ""
        if origem is None or destino is None:
            erros.append("transição referencia estado inexistente")
            continue
        atual.append((origem, leitura, destino))

    esperado = [
        (origem, "" if simbolo == EPSILON else JFLAP_LABELS.get(simbolo, simbolo), destino)
        for origem, simbolo, destino in spec["transicoes"]
    ]

    if set(atual) != set(esperado) or len(atual) != len(esperado):
        faltantes = sorted(set(esperado) - set(atual))
        extras = sorted(set(atual) - set(esperado))
        erros.append(f"transições JFLAP divergentes: faltantes={faltantes[:5]}, extras={extras[:5]}")

    return erros


def main() -> int:
    falhas = 0

    print("=== ESTRUTURA PYTHON ===")
    for nome, spec in CANONICAS.items():
        erros = validar_codigo(nome, spec)
        if erros:
            falhas += 1
            print(f"{nome}: FALHA")
            for erro in erros:
                print(f"  - {erro}")
        else:
            c = THOMPSON_COUNTS[nome]
            print(
                f"{nome}: OK — {c['estados']} estados / {c['transicoes']} transições "
                f"/ {c['epsilon']} ε / {c['rotuladas']} rotuladas"
            )

    print("\n=== JFLAP (.jff) ===")
    for nome, spec in CANONICAS.items():
        erros = validar_jflap(nome, spec)
        if erros:
            falhas += 1
            print(f"{nome}: FALHA")
            for erro in erros:
                print(f"  - {erro}")
        else:
            print(f"{nome}: OK — tabela JFLAP coincide com a tabela canônica")

    if falhas:
        print(f"\nVALIDAÇÃO ESTRUTURAL: {falhas} falha(s)")
        return 1

    print("\nVALIDAÇÃO ESTRUTURAL: 6/6 AFNε Python + 6/6 JFLAP")
    print("Todas as tabelas, estados, finais e transições coincidem exatamente.")
    return 0


if __name__ == "__main__":
    # Garante a impressão de "ε" e acentos mesmo com saída redirecionada no Windows.
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
