"""Validação reproduzível da ER-03: decimal, AFNε × regex Python."""

from __future__ import annotations

import itertools
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.automata import REGEX_ER03, THOMPSON_COUNTS, construir_er03


# Bateria alinhada à especificação documentada da ER-03:
# pelo menos 6 cadeias aceitas, 6 rejeitadas e casos-limite.
CASOS_OFICIAIS = {
    "0.5": True,
    "0.50": True,
    "1.5": True,
    "9.5": True,
    "10.25": True,
    "2026.75": True,
    "00.5": False,
    "01.5": False,
    ".5": False,
    "5.": False,
    "1.2.3": False,
    "-9.5": False,
}

CASOS_LIMITE = {
    "0.5": True,    # menor forma decimal válida documentada
    "0.50": True,   # mais de um dígito na parte fracionária
    ".5": False,    # ponto sem parte inteira
    "5.": False,    # ponto sem dígito fracionário
    "00.5": False,  # zero à esquerda na parte inteira
}


def main() -> int:
    afne = construir_er03()
    esperado_estrutura = THOMPSON_COUNTS["ER-03"]

    falhas_estrutura = []
    if len(afne.estados) != esperado_estrutura["estados"]:
        falhas_estrutura.append(
            f"estados={len(afne.estados)} (esperado {esperado_estrutura['estados']})"
        )
    if afne.inicial != "q0":
        falhas_estrutura.append(f"inicial={afne.inicial!r} (esperado 'q0')")
    if afne.finais != frozenset({"q17"}):
        falhas_estrutura.append(
            f"finais={sorted(afne.finais)} (esperado ['q17'])"
        )

    divergencias = []
    for cadeia, esperado in CASOS_OFICIAIS.items():
        afn = afne.aceita(cadeia)
        regex = re.fullmatch(REGEX_ER03, cadeia) is not None
        if afn != esperado or regex != esperado or afn != regex:
            divergencias.append((cadeia, afn, regex, esperado))

    falhas_limite = []
    for cadeia, esperado in CASOS_LIMITE.items():
        afn = afne.aceita(cadeia)
        regex = re.fullmatch(REGEX_ER03, cadeia) is not None
        if afn != esperado or regex != esperado or afn != regex:
            falhas_limite.append((cadeia, afn, regex, esperado))

    total_exaustivo = 0
    divergencias_exaustivas = []
    alfabeto_reduzido = "01."

    # Todas as cadeias de tamanho 0..5 sobre {0,1,.}, conforme a validação reduzida.
    for tamanho in range(6):
        for tupla in itertools.product(alfabeto_reduzido, repeat=tamanho):
            cadeia = "".join(tupla)
            total_exaustivo += 1
            afn = afne.aceita(cadeia)
            regex = re.fullmatch(REGEX_ER03, cadeia) is not None
            if afn != regex:
                divergencias_exaustivas.append((cadeia, afn, regex))

    aceitas = sum(CASOS_OFICIAIS.values())
    rejeitadas = len(CASOS_OFICIAIS) - aceitas

    print(f"ER-03 | casos oficiais: {len(CASOS_OFICIAIS)} ({aceitas} aceitas / {rejeitadas} rejeitadas)")
    print(f"ER-03 | casos-limite verificados: {len(CASOS_LIMITE)}")
    print(f"ER-03 | estados: {len(afne.estados)} / esperado: {esperado_estrutura['estados']}")
    print(f"ER-03 | final: {sorted(afne.finais)} / esperado: ['q17']")
    print(f"ER-03 | divergências oficiais: {len(divergencias)}")
    print(f"ER-03 | divergências de fronteira: {len(falhas_limite)}")
    print(f"ER-03 | exaustivo (0..5): {total_exaustivo} cadeias")
    print(f"ER-03 | divergências exaustivas: {len(divergencias_exaustivas)}")

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

    print("VALIDAÇÃO ER-03: 12/12 casos oficiais + casos-limite")
    print("VALIDAÇÃO EXAUSTIVA ER-03: 0 divergências")
    return 0


if __name__ == "__main__":
    # Garante a impressão de "ε" e acentos mesmo com saída redirecionada no Windows.
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
