"""Validação reproduzível da ER-04: número científico, AFNε × regex Python."""

from __future__ import annotations

import itertools
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.automata import REGEX_ER04, THOMPSON_COUNTS, construir_er04


# Bateria conforme a especificação do projeto: 6 aceitas + 6 rejeitadas.
# A forma científica exige expoente inteiro e aceita parte decimal opcional.
CASOS_OFICIAIS = {
    "0e0": True,
    "1e10": True,
    "9E9": True,
    "1.5e3": True,
    "12.25E-2": True,
    "2026.75e+10": True,
    "e10": False,
    "1e": False,
    "1.e3": False,
    ".5e2": False,
    "01e2": False,
    "1.2e3.4": False,
}

CASOS_LIMITE = {
    "0e0": True,       # menor forma científica válida
    "9E9": True,       # expoente sem sinal e forma compacta
    "1e+0": True,      # sinal positivo explícito
    "1e-0": True,      # sinal negativo explícito
    "00e1": False,     # zero à esquerda
    "1.e1": False,     # ponto sem dígito após a parte decimal
    "1.2e": False,     # ausência do expoente numérico
}


def main() -> int:
    afne = construir_er04()
    esperado_estrutura = THOMPSON_COUNTS["ER-04"]

    falhas_estrutura = []
    if len(afne.estados) != esperado_estrutura["estados"]:
        falhas_estrutura.append(
            f"estados={len(afne.estados)} (esperado {esperado_estrutura['estados']})"
        )
    if afne.inicial != "q0":
        falhas_estrutura.append(f"inicial={afne.inicial!r} (esperado 'q0')")
    if afne.finais != frozenset({"q39"}):
        falhas_estrutura.append(
            f"finais={sorted(afne.finais)} (esperado ['q39'])"
        )

    divergencias = []
    for cadeia, esperado in CASOS_OFICIAIS.items():
        afn = afne.aceita(cadeia)
        regex = re.fullmatch(REGEX_ER04, cadeia) is not None
        if afn != esperado or regex != esperado or afn != regex:
            divergencias.append((cadeia, afn, regex, esperado))

    falhas_limite = []
    for cadeia, esperado in CASOS_LIMITE.items():
        afn = afne.aceita(cadeia)
        regex = re.fullmatch(REGEX_ER04, cadeia) is not None
        if afn != esperado or regex != esperado or afn != regex:
            falhas_limite.append((cadeia, afn, regex, esperado))

    total_exaustivo = 0
    divergencias_exaustivas = []
    alfabeto_reduzido = "01.eE+-"

    # Busca exaustiva reduzida sobre o mesmo alfabeto usado na documentação.
    for tamanho in range(6):
        for tupla in itertools.product(alfabeto_reduzido, repeat=tamanho):
            cadeia = "".join(tupla)
            total_exaustivo += 1
            afn = afne.aceita(cadeia)
            regex = re.fullmatch(REGEX_ER04, cadeia) is not None
            if afn != regex:
                divergencias_exaustivas.append((cadeia, afn, regex))

    aceitas = sum(CASOS_OFICIAIS.values())
    rejeitadas = len(CASOS_OFICIAIS) - aceitas

    print(f"ER-04 | casos oficiais: {len(CASOS_OFICIAIS)} ({aceitas} aceitas / {rejeitadas} rejeitadas)")
    print(f"ER-04 | casos-limite verificados: {len(CASOS_LIMITE)}")
    print(f"ER-04 | estados: {len(afne.estados)} / esperado: {esperado_estrutura['estados']}")
    print(f"ER-04 | final: {sorted(afne.finais)} / esperado: ['q39']")
    print(f"ER-04 | divergências oficiais: {len(divergencias)}")
    print(f"ER-04 | divergências de fronteira: {len(falhas_limite)}")
    print(f"ER-04 | exaustivo (0..5): {total_exaustivo} cadeias")
    print(f"ER-04 | divergências exaustivas: {len(divergencias_exaustivas)}")

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

    print("VALIDAÇÃO ER-04: 12/12 casos oficiais + casos-limite")
    print("VALIDAÇÃO EXAUSTIVA ER-04: 0 divergências")
    return 0


if __name__ == "__main__":
    # Garante a impressão de "ε" e acentos mesmo com saída redirecionada no Windows.
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
