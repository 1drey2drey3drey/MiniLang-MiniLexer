"""Valida os .jff com o próprio JFLAP: python tests/validate_jflap_runtime.py caminho/JFLAP7.1.jar.

Requer Java 11+ com suporte à execução de arquivos fonte (JDK).
"""

import base64
import importlib
import itertools
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src import automata


def casos(numero):
    modulo = importlib.import_module(f"validate_er{numero:02}")
    casos = dict(modulo.CASOS_OFICIAIS)
    casos.update(getattr(modulo, "CASOS_LIMITE", {}))
    regex = getattr(automata, f"REGEX_ER{numero:02}")
    # Enumeração reduzida, incluindo entradas inválidas e cadeia vazia.
    alfabeto = {1: "aZ0_", 2: "019", 3: "01.", 4: "01.eE+-", 5: 'a0 "\\', 6: "0259:"}[numero]
    for tamanho in range(6):
        for partes in itertools.product(alfabeto, repeat=tamanho):
            cadeia = "".join(partes)
            casos.setdefault(cadeia, re.fullmatch(regex, cadeia) is not None)
    # Exercita cada caractere ASCII, especialmente espaço, pontuação e XML.
    formatos = {1: "{}", 2: "{}", 3: "1.{}", 4: "1e{}", 5: '"{}"', 6: "12:3{}"}
    for codigo in range(128):
        cadeia = formatos[numero].format(chr(codigo))
        casos.setdefault(cadeia, re.fullmatch(regex, cadeia) is not None)
    if numero == 6:
        for hora in range(100):
            for minuto in range(100):
                casos[f"{hora:02}:{minuto:02}"] = hora < 24 and minuto < 60
    return casos


def main():
    if len(sys.argv) != 2 or not Path(sys.argv[1]).is_file():
        raise SystemExit("Uso: python tests/validate_jflap_runtime.py caminho/JFLAP7.1.jar")
    with tempfile.TemporaryDirectory(prefix="minilang-jflap-") as temp:
        for numero in range(1, 7):
            linhas = [f"{int(esperado)}\t{base64.b64encode(cadeia.encode()).decode()}\n"
                      for cadeia, esperado in casos(numero).items()]
            Path(temp, f"ER-{numero:02}.tsv").write_text("".join(linhas), encoding="utf-8")
        return subprocess.run([
            "java", "-Djava.awt.headless=true", "-cp", str(Path(sys.argv[1]).resolve()),
            str(ROOT / "tests" / "JflapRuntimeCheck.java"), str(ROOT), temp,
        ], cwd=ROOT).returncode


if __name__ == "__main__":
    raise SystemExit(main())
