"""Validação reproduzível da ER-01: AFNε × regex Python."""

from __future__ import annotations

import itertools
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.automata import REGEX_ER01, THOMPSON_COUNTS, construir_er01


# Casos definidos na especificação do projeto e alinhados à exigência da lauda:
# pelo menos 6 cadeias aceitas, 6 rejeitadas e casos-limite.
CASOS_OFICIAIS = {
    "a": True,
    "nome": True,
    "aluno1": True,
    "valor_total": True,
    "mediaFinal2": True,
    "a1_b2": True,
    "": False,
    "1aluno": False,
    "_nome": False,
    "nome_": False,
    "nome__aluno": False,
    "nome-aluno": False,
}

CASOS_LIMITE = {
    "a": True,      # menor identificador válido
    "": False,      # cadeia vazia
    "a_": False,    # sublinhado no final
    "a__b": False,  # dois sublinhados consecutivos
}


def main() -> int:
    afne = construir_er01()
    esperado_estrutura = THOMPSON_COUNTS["ER-01"]

    falhas_estrutura = []
    if len(afne.estados) != esperado_estrutura["estados"]:
        falhas_estrutura.append(
            f"estados={len(afne.estados)} (esperado {esperado_estrutura['estados']})"
        )
    if afne.inicial != "q0":
        falhas_estrutura.append(f"inicial={afne.inicial!r} (esperado 'q0')")
    if afne.finais != frozenset({"q27"}):
        falhas_estrutura.append(
            f"finais={sorted(afne.finais)} (esperado ['q27'])"
        )

    divergencias = []
    for cadeia, esperado in CASOS_OFICIAIS.items():
        afn = afne.aceita(cadeia)
        regex = re.fullmatch(REGEX_ER01, cadeia) is not None
        if afn != esperado or regex != esperado or afn != regex:
            divergencias.append((cadeia, afn, regex, esperado))

    falhas_limite = []
    for cadeia, esperado in CASOS_LIMITE.items():
        afn = afne.aceita(cadeia)
        regex = re.fullmatch(REGEX_ER01, cadeia) is not None
        if afn != esperado or regex != esperado or afn != regex:
            falhas_limite.append((cadeia, afn, regex, esperado))

    total_exaustivo = 0
    divergencias_exaustivas = []
    alfabeto_reduzido = "ab01_"

    # Todas as cadeias de tamanho 0..5 sobre um alfabeto reduzido.
    for tamanho in range(6):
        for tupla in itertools.product(alfabeto_reduzido, repeat=tamanho):
            cadeia = "".join(tupla)
            total_exaustivo += 1
            afn = afne.aceita(cadeia)
            regex = re.fullmatch(REGEX_ER01, cadeia) is not None
            if afn != regex:
                divergencias_exaustivas.append((cadeia, afn, regex))

    aceitas = sum(CASOS_OFICIAIS.values())
    rejeitadas = len(CASOS_OFICIAIS) - aceitas

    print(f"ER-01 | casos oficiais: {len(CASOS_OFICIAIS)} ({aceitas} aceitas / {rejeitadas} rejeitadas)")
    print(f"ER-01 | casos-limite verificados: {len(CASOS_LIMITE)}")
    print(f"ER-01 | estados: {len(afne.estados)} / esperado: {esperado_estrutura['estados']}")
    print(f"ER-01 | final: {sorted(afne.finais)} / esperado: ['q27']")
    print(f"ER-01 | divergências oficiais: {len(divergencias)}")
    print(f"ER-01 | divergências de fronteira: {len(falhas_limite)}")
    print(f"ER-01 | exaustivo (0..5): {total_exaustivo} cadeias")
    print(f"ER-01 | divergências exaustivas: {len(divergencias_exaustivas)}")

    if falhas_estrutura:
        print("Falhas estruturais:")
        for falha in falhas_estrutura:
            print(" ", falha)

    if divergencias:
        print("Divergências oficiais:")
        for item in divergencias:
            print(" ", item)

    if falhas_limite:
        print("Falhas de fronteira:")
        for item in falhas_limite:
            print(" ", item)

    if divergencias_exaustivas:
        print("Primeiras divergências exaustivas:")
        for item in divergencias_exaustivas[:20]:
            print(" ", item)

    if (
        falhas_estrutura
        or divergencias
        or falhas_limite
        or divergencias_exaustivas
    ):
        return 1

    print("VALIDAÇÃO ER-01: 12/12 casos oficiais + casos-limite")
    print("VALIDAÇÃO EXAUSTIVA ER-01: 0 divergências")
    return 0


if __name__ == "__main__":
    # Garante a impressão de "ε" e acentos mesmo com saída redirecionada no Windows.
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
