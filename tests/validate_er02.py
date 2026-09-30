"""Validação reproduzível da ER-02: AFNε × regex Python."""

from __future__ import annotations

import itertools
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.automata import REGEX_ER02, construir_er02


CASOS_OFICIAIS = {
    "0": True,
    "1": True,
    "7": True,
    "9": True,
    "10": True,
    "20": True,
    "2026": True,
    "999": True,
    "": False,
    "00": False,
    "01": False,
    "007": False,
    "0123": False,
    "-1": False,
    "1.5": False,
}


def main() -> int:
    afne = construir_er02()

    divergencias = []
    for cadeia, esperado in CASOS_OFICIAIS.items():
        afn = afne.aceita(cadeia)
        regex = re.fullmatch(REGEX_ER02, cadeia) is not None
        if afn != esperado or regex != esperado or afn != regex:
            divergencias.append((cadeia, afn, regex, esperado))

    total_exaustivo = 0
    divergencias_exaustivas = []
    alfabeto_reduzido = "0123456789"

    # Todas as cadeias numéricas de tamanho 0..5.
    for tamanho in range(6):
        for tupla in itertools.product(alfabeto_reduzido, repeat=tamanho):
            cadeia = "".join(tupla)
            total_exaustivo += 1
            afn = afne.aceita(cadeia)
            regex = re.fullmatch(REGEX_ER02, cadeia) is not None
            if afn != regex:
                divergencias_exaustivas.append((cadeia, afn, regex))

    print(f"Casos oficiais: {len(CASOS_OFICIAIS)}")
    print(f"Divergências oficiais: {len(divergencias)}")
    print(f"Exaustivo numérico (0..5): {total_exaustivo} cadeias")
    print(f"Divergências exaustivas: {len(divergencias_exaustivas)}")

    if divergencias:
        print("Divergências oficiais:")
        for item in divergencias:
            print(item)

    if divergencias_exaustivas:
        print("Primeiras divergências exaustivas:")
        for item in divergencias_exaustivas[:20]:
            print(item)

    if divergencias or divergencias_exaustivas:
        return 1

    print("VALIDAÇÃO ER-02: 15/15")
    print("VALIDAÇÃO EXAUSTIVA: 0 divergências")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
