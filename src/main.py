"""Interface de linha de comando simples para o MiniLexer."""

from __future__ import annotations

import argparse
from pathlib import Path

from .lexer import LexicalError, format_tokens, tokenize


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="MiniLexer — analisador léxico da MiniLang")
    parser.add_argument("arquivo", nargs="?", help="arquivo .min a ser analisado")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.arquivo:
        path = Path(args.arquivo)
        try:
            source = path.read_text(encoding="utf-8")
        except OSError as exc:
            parser.error(f"não foi possível ler o arquivo: {exc}")
    else:
        source = input("Digite o código MiniLang (uma linha):\n")

    if source == "":
        print("Nenhum código foi fornecido.\n\nA análise léxica não foi realizada.")
        return 0

    try:
        tokens = tokenize(source)
    except LexicalError as exc:
        print(exc)
        return 1

    print(format_tokens(tokens))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
