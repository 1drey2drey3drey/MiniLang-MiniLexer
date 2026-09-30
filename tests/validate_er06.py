"""Validação reproduzível da ER-06: horário, AFNε × regex Python."""

from __future__ import annotations

import itertools
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.automata import REGEX_ER06, THOMPSON_COUNTS, construir_er06


# Bateria exigida pela lauda: pelo menos 6 aceitas e 6 rejeitadas,
# incluindo casos-limite.
CASOS_OFICIAIS = {
    "00:00": True,
    "09:05": True,
    "12:30": True,
    "14:59": True,
    "23:00": True,
    "23:59": True,
    "24:00": False,
    "12:60": False,
    "2:30": False,
    "14:5": False,
    "99:99": False,
    "14:30:00": False,
}

CASOS_LIMITE = {
    "00:00": True,   # menor horário válido
    "09:59": True,   # limite baixo com dois dígitos
    "23:59": True,   # maior horário válido
    "24:00": False,  # hora imediatamente fora do intervalo
    "23:60": False,  # minuto imediatamente fora do intervalo
    "2:30": False,   # hora sem dois dígitos
}


def main() -> int:
    afne = construir_er06()
    esperado_estrutura = THOMPSON_COUNTS["ER-06"]

    falhas_estrutura = []
    if len(afne.estados) != esperado_estrutura["estados"]:
        falhas_estrutura.append(
            f"estados={len(afne.estados)} (esperado {esperado_estrutura['estados']})"
        )
    if afne.inicial != "q0":
        falhas_estrutura.append(f"inicial={afne.inicial!r} (esperado 'q0')")
    if afne.finais != frozenset({"q15"}):
        falhas_estrutura.append(
            f"finais={sorted(afne.finais)} (esperado ['q15'])"
        )

    divergencias = []
    for cadeia, esperado in CASOS_OFICIAIS.items():
        afn = afne.aceita(cadeia)
        regex = re.fullmatch(REGEX_ER06, cadeia) is not None
        if afn != esperado or regex != esperado or afn != regex:
            divergencias.append((cadeia, afn, regex, esperado))

    falhas_limite = []
    for cadeia, esperado in CASOS_LIMITE.items():
        afn = afne.aceita(cadeia)
        regex = re.fullmatch(REGEX_ER06, cadeia) is not None
        if afn != esperado or regex != esperado or afn != regex:
            falhas_limite.append((cadeia, afn, regex, esperado))

    total_exaustivo = 0
    divergencias_exaustivas = []
    alfabeto_reduzido = "0123456789:"

    # Todas as cadeias de tamanho 0..5 sobre o alfabeto reduzido documentado.
    for tamanho in range(6):
        for tupla in itertools.product(alfabeto_reduzido, repeat=tamanho):
            cadeia = "".join(tupla)
            total_exaustivo += 1
            afn = afne.aceita(cadeia)
            regex = re.fullmatch(REGEX_ER06, cadeia) is not None
            if afn != regex:
                divergencias_exaustivas.append((cadeia, afn, regex))

    aceitas = sum(CASOS_OFICIAIS.values())
    rejeitadas = len(CASOS_OFICIAIS) - aceitas

    print(
        f"ER-06 | casos oficiais: {len(CASOS_OFICIAIS)} "
        f"({aceitas} aceitas / {rejeitadas} rejeitadas)"
    )
    print(f"ER-06 | casos-limite verificados: {len(CASOS_LIMITE)}")
    print(
        f"ER-06 | estrutura: {len(afne.estados)} estados / "
        f"{esperado_estrutura['transicoes']} transições / "
        f"{esperado_estrutura['epsilon']} ε / "
        f"{esperado_estrutura['rotuladas']} rotuladas"
    )
    print(f"ER-06 | final: {sorted(afne.finais)} / esperado: ['q15']")
    print(f"ER-06 | divergências oficiais: {len(divergencias)}")
    print(f"ER-06 | divergências de fronteira: {len(falhas_limite)}")
    print(f"ER-06 | exaustivo (0..5): {total_exaustivo} cadeias")
    print(f"ER-06 | divergências exaustivas: {len(divergencias_exaustivas)}")

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

    print("VALIDAÇÃO ER-06: 12/12 casos oficiais + casos-limite")
    print("VALIDAÇÃO EXAUSTIVA ER-06: 0 divergências")
    return 0


if __name__ == "__main__":
    # Garante a impressão de "ε" e acentos mesmo com saída redirecionada no Windows.
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
