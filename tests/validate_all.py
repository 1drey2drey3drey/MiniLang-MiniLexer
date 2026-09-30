"""Validação cruzada reproduzível das seis ERs principais."""

from __future__ import annotations

import itertools
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.automata import (  # noqa: E402
    REGEX_ER01,
    REGEX_ER02,
    REGEX_ER03,
    REGEX_ER04,
    REGEX_ER05,
    REGEX_ER06,
    construir_er01,
    construir_er02,
    construir_er03,
    construir_er04,
    construir_er05,
    construir_er06,
)


DEFINICOES = [
    ("ER-01", construir_er01, REGEX_ER01, "ab01_", 5),
    ("ER-02", construir_er02, REGEX_ER02, "0123456789", 5),
    ("ER-03", construir_er03, REGEX_ER03, "01.", 5),
    ("ER-04", construir_er04, REGEX_ER04, "01.eE+-", 5),
    ("ER-05", construir_er05, REGEX_ER05, "a0 _.", 6),
    ("ER-06", construir_er06, REGEX_ER06, "0123456789:", 5),
]


def validar(nome, construir, regex, alfabeto, tamanho_max):
    afne = construir()
    divergencias = []
    total = 0

    for tamanho in range(tamanho_max + 1):
        for tupla in itertools.product(alfabeto, repeat=tamanho):
            cadeia = "".join(tupla)
            total += 1
            afn = afne.aceita(cadeia)
            esperado = re.fullmatch(regex, cadeia) is not None
            if afn != esperado:
                divergencias.append((cadeia, afn, esperado))
                if len(divergencias) >= 20:
                    return total, divergencias

    return total, divergencias


def main() -> int:
    falhas = 0

    for nome, construir, regex, alfabeto, tamanho_max in DEFINICOES:
        total, divergencias = validar(nome, construir, regex, alfabeto, tamanho_max)
        print(f"{nome}: {total} cadeias | divergências: {len(divergencias)}")
        if divergencias:
            falhas += 1
            print("  primeiras divergências:")
            for divergencia in divergencias[:5]:
                print(" ", divergencia)

    if falhas:
        return 1

    print("VALIDAÇÃO CRUZADA: 6/6 ERs sem divergências nas buscas exaustivas limitadas.")
    return 0


if __name__ == "__main__":
    # Garante a impressão de "ε" e acentos mesmo com saída redirecionada no Windows.
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
