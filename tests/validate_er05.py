"""Validação reproduzível da ER-05: literal de string, AFNε × regex Python."""

from __future__ import annotations

import itertools
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.automata import REGEX_ER05, THOMPSON_COUNTS, construir_er05


# Bateria alinhada à especificação documentada da ER-05:
# 6 cadeias aceitas e 6 rejeitadas.
CASOS_OFICIAIS = {
    '""': True,
    '"Andrey"': True,
    '"abc 123"': True,
    '"a_b.c"': True,
    '"hello!"': True,
    '"12:30"': True,
    "": False,
    '"abc': False,
    'abc"': False,
    '"a"b"': False,
    '"a\\b"': False,
    '"linha\n': False,
}

CASOS_LIMITE = {
    '""': True,          # limite positivo: C* = ε no interior
    '"a"': True,         # conteúdo unitário
    '" "': True,         # espaço pertence a C
    '"a+b=c"': True,     # operadores pertencem a C
    '"a\\b"': False,     # barra invertida não pertence a C
    '"linha\n': False,   # quebra de linha não pertence a C
}


def main() -> int:
    afne = construir_er05()
    esperado_estrutura = THOMPSON_COUNTS["ER-05"]

    falhas_estrutura = []
    if len(afne.estados) != esperado_estrutura["estados"]:
        falhas_estrutura.append(
            f"estados={len(afne.estados)} (esperado {esperado_estrutura['estados']})"
        )
    if afne.inicial != "q0":
        falhas_estrutura.append(f"inicial={afne.inicial!r} (esperado 'q0')")
    if afne.finais != frozenset({"q7"}):
        falhas_estrutura.append(
            f"finais={sorted(afne.finais)} (esperado ['q7'])"
        )

    divergencias = []
    for cadeia, esperado in CASOS_OFICIAIS.items():
        afn = afne.aceita(cadeia)
        regex = re.fullmatch(REGEX_ER05, cadeia) is not None
        if afn != esperado or regex != esperado or afn != regex:
            divergencias.append((cadeia, afn, regex, esperado))

    falhas_limite = []
    for cadeia, esperado in CASOS_LIMITE.items():
        afn = afne.aceita(cadeia)
        regex = re.fullmatch(REGEX_ER05, cadeia) is not None
        if afn != esperado or regex != esperado or afn != regex:
            falhas_limite.append((cadeia, afn, regex, esperado))

    total_exaustivo = 0
    divergencias_exaustivas = []
    # Mesmo alfabeto reduzido registrado na documentação da ER-05.
    alfabeto_reduzido = 'a0 _."\\'

    for tamanho in range(6):
        for tupla in itertools.product(alfabeto_reduzido, repeat=tamanho):
            cadeia = "".join(tupla)
            total_exaustivo += 1
            afn = afne.aceita(cadeia)
            regex = re.fullmatch(REGEX_ER05, cadeia) is not None
            if afn != regex:
                divergencias_exaustivas.append((cadeia, afn, regex))

    aceitas = sum(CASOS_OFICIAIS.values())
    rejeitadas = len(CASOS_OFICIAIS) - aceitas

    print(f"ER-05 | casos oficiais: {len(CASOS_OFICIAIS)} ({aceitas} aceitas / {rejeitadas} rejeitadas)")
    print(f"ER-05 | casos-limite verificados: {len(CASOS_LIMITE)}")
    print(f"ER-05 | estados: {len(afne.estados)} / esperado: {esperado_estrutura['estados']}")
    print(f"ER-05 | final: {sorted(afne.finais)} / esperado: ['q7']")
    print(f"ER-05 | divergências oficiais: {len(divergencias)}")
    print(f"ER-05 | divergências de fronteira: {len(falhas_limite)}")
    print(f"ER-05 | exaustivo (0..5): {total_exaustivo} cadeias")
    print(f"ER-05 | divergências exaustivas: {len(divergencias_exaustivas)}")

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

    print("VALIDAÇÃO ER-05: 12/12 casos oficiais + casos-limite")
    print("VALIDAÇÃO EXAUSTIVA ER-05: 0 divergências")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
