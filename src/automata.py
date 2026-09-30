"""Simulador de AFNε e construções Thompson da MiniLang.

Esta etapa mantém o simulador genérico e adiciona os seis AFNε previstos na
especificação. Classes como L, N, D e C são rótulos agrupados na construção
formal e são expandidas para símbolos individuais na implementação.
"""

from __future__ import annotations

from typing import Dict, FrozenSet, Iterable, Set

EPSILON = ""

# Regex de referência utilizadas exclusivamente para validação cruzada.
REGEX_ER01 = r"[A-Za-z]([A-Za-z0-9]|_[A-Za-z0-9]+)*"
REGEX_ER02 = r"(0|[1-9][0-9]*)"
REGEX_ER03 = r"(0|[1-9][0-9]*)\.[0-9]+"
REGEX_ER04 = r"(0|[1-9][0-9]*)(\.[0-9]+)?[eE][+-]?[0-9]+"
REGEX_ER05 = r'"[A-Za-z0-9 _.,!?;:+*/=<>-]*"'
REGEX_ER06 = r"([01][0-9]|2[0-3]):[0-5][0-9]"

THOMPSON_COUNTS = {
    "ER-01": {"estados": 28, "transicoes": 35, "epsilon": 27, "rotuladas": 8},
    "ER-02": {"estados": 10, "transicoes": 12, "epsilon": 9, "rotuladas": 3},
    "ER-03": {"estados": 18, "transicoes": 22, "epsilon": 16, "rotuladas": 6},
    "ER-04": {"estados": 42, "transicoes": 52, "epsilon": 40, "rotuladas": 12},
    "ER-05": {"estados": 8, "transicoes": 9, "epsilon": 6, "rotuladas": 3},
    "ER-06": {"estados": 16, "transicoes": 16, "epsilon": 9, "rotuladas": 7},
}


class AFNe:
    """Simulador de Autômato Finito Não Determinístico com ε-transições."""

    def __init__(
        self,
        estados: Iterable[str],
        alfabeto: Iterable[str],
        transicoes: Dict[tuple[str, str], Iterable[str]],
        inicial: str,
        finais: Iterable[str],
    ) -> None:
        self.estados: FrozenSet[str] = frozenset(estados)
        self.alfabeto: FrozenSet[str] = frozenset(alfabeto)
        self.inicial = inicial
        self.finais: FrozenSet[str] = frozenset(finais)
        self.transicoes = {
            chave: frozenset(destinos) for chave, destinos in transicoes.items()
        }
        self._validar_estrutura()

    def _validar_estrutura(self) -> None:
        """Valida Q, Σ e δ antes da simulação."""
        if self.inicial not in self.estados:
            raise ValueError(f"Estado inicial inexistente: {self.inicial}")

        invalidos = self.finais - self.estados
        if invalidos:
            raise ValueError(f"Estados finais inexistentes: {sorted(invalidos)}")

        if EPSILON in self.alfabeto:
            raise ValueError("ε não pode pertencer ao alfabeto de entrada.")

        for chave, destinos in self.transicoes.items():
            if not isinstance(chave, tuple) or len(chave) != 2:
                raise ValueError(f"Chave de transição inválida: {chave!r}")

            origem, simbolo = chave
            if origem not in self.estados:
                raise ValueError(f"Origem inexistente: {origem}")

            if simbolo != EPSILON and simbolo not in self.alfabeto:
                raise ValueError(f"Símbolo fora do alfabeto: {simbolo!r}")

            invalidos = destinos - self.estados
            if invalidos:
                raise ValueError(
                    f"Destinos inexistentes em {origem!r}, {simbolo!r}: "
                    f"{sorted(invalidos)}"
                )

    def epsilon_fecho(self, estados: Iterable[str]) -> Set[str]:
        """Calcula o ε-fecho de um conjunto de estados."""
        fecho = set(estados)
        invalidos = fecho - self.estados
        if invalidos:
            raise ValueError(f"Estados inexistentes no ε-fecho: {sorted(invalidos)}")

        pilha = list(fecho)
        while pilha:
            estado = pilha.pop()
            for destino in self.transicoes.get((estado, EPSILON), frozenset()):
                if destino not in fecho:
                    fecho.add(destino)
                    pilha.append(destino)

        return fecho

    def mover(self, estados: Iterable[str], simbolo: str) -> Set[str]:
        """Executa MOVE para um único símbolo de entrada."""
        estados = set(estados)
        invalidos = estados - self.estados
        if invalidos:
            raise ValueError(f"Estados inexistentes no MOVE: {sorted(invalidos)}")

        if simbolo == EPSILON:
            raise ValueError("mover() não recebe ε; use epsilon_fecho().")
        if simbolo not in self.alfabeto:
            raise ValueError(f"Símbolo fora do alfabeto: {simbolo!r}")

        destinos: Set[str] = set()
        for estado in estados:
            destinos.update(self.transicoes.get((estado, simbolo), frozenset()))
        return destinos

    def aceita(self, cadeia: str) -> bool:
        """Retorna True quando o AFNε aceita a cadeia inteira."""
        atuais = self.epsilon_fecho({self.inicial})

        for simbolo in cadeia:
            if simbolo not in self.alfabeto:
                return False

            atuais = self.mover(atuais, simbolo)
            if not atuais:
                return False

            atuais = self.epsilon_fecho(atuais)

        return bool(atuais & self.finais)

    def simular(self, cadeia: str) -> list[Set[str]]:
        """Retorna o histórico dos conjuntos após cada símbolo consumido."""
        historico = [self.epsilon_fecho({self.inicial})]
        atuais = historico[0]

        for simbolo in cadeia:
            if simbolo not in self.alfabeto:
                historico.append(set())
                break

            atuais = self.mover(atuais, simbolo)
            atuais = self.epsilon_fecho(atuais)
            historico.append(atuais)

        return historico


def _expandir_transicoes(
    agrupadas: Iterable[tuple[str, str, str]],
    classes: dict[str, str],
) -> tuple[dict[tuple[str, str], set[str]], set[str]]:
    """Expande rótulos agrupados para símbolos individuais."""
    transicoes: dict[tuple[str, str], set[str]] = {}
    alfabeto: set[str] = set()

    for origem, rotulo, destino in agrupadas:
        if rotulo == EPSILON:
            simbolos = [EPSILON]
        elif rotulo in classes:
            simbolos = list(classes[rotulo])
            alfabeto.update(simbolos)
        else:
            simbolos = [rotulo]
            alfabeto.add(rotulo)

        for simbolo in simbolos:
            transicoes.setdefault((origem, simbolo), set()).add(destino)

    return transicoes, alfabeto


def _construir(
    estados: Iterable[str],
    agrupadas: Iterable[tuple[str, str, str]],
    classes: dict[str, str],
    inicial: str,
    final: str,
) -> AFNe:
    transicoes, alfabeto = _expandir_transicoes(agrupadas, classes)
    return AFNe(estados, alfabeto, transicoes, inicial, {final})


def construir_er01() -> AFNe:
    """Constrói o AFNε definitivo da ER-01 — Identificador estruturado."""
    L = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    D = "0123456789"
    agrupadas = [
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
    ]
    return _construir(
        {f"q{i}" for i in range(28)}, agrupadas, {"L": L, "D": D}, "q0", "q27"
    )


def construir_er02() -> AFNe:
    """Constrói o AFNε definitivo da ER-02 — Inteiro."""
    D = "0123456789"
    N = "123456789"
    agrupadas = [
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
    ]
    return _construir(
        {f"q{i}" for i in range(10)},
        agrupadas,
        {"N": N, "D": D},
        "q0",
        "q1",
    )


def construir_er03() -> AFNe:
    """Constrói o AFNε definitivo da ER-03 — Decimal."""
    D = "0123456789"
    N = "123456789"
    agrupadas = [
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
    ]
    return _construir(
        {f"q{i}" for i in range(18)},
        agrupadas,
        {"N": N, "D": D, "P": "."},
        "q0",
        "q17",
    )


def construir_er04() -> AFNe:
    """Constrói o AFNε definitivo da ER-04 — Número científico."""
    D = "0123456789"
    N = "123456789"
    agrupadas = [
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
    ]
    return _construir(
        {f"q{i}" for i in range(42)},
        agrupadas,
        {"N": N, "D": D, "P": "."},
        "q0",
        "q39",
    )


def construir_er05() -> AFNe:
    """Constrói o AFNε definitivo da ER-05 — Literal de string."""
    C = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 _.,!?;:+*/=<>-"
    agrupadas = [
        ("q0", '"', "q1"),
        ("q4", "C", "q5"),
        ("q2", EPSILON, "q4"),
        ("q2", EPSILON, "q3"),
        ("q5", EPSILON, "q4"),
        ("q5", EPSILON, "q3"),
        ("q1", EPSILON, "q2"),
        ("q6", '"', "q7"),
        ("q3", EPSILON, "q6"),
    ]
    return _construir({f"q{i}" for i in range(8)}, agrupadas, {"C": C}, "q0", "q7")


def construir_er06() -> AFNe:
    """Constrói o AFNε definitivo da ER-06 — Horário."""
    D = "0123456789"
    agrupadas = [
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
    ]
    return _construir(
        {f"q{i}" for i in range(16)},
        agrupadas,
        {"D": D, "01": "01", "0123": "0123", "012345": "012345"},
        "q0",
        "q15",
    )
