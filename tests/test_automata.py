import pytest

from src.automata import AFNe, EPSILON


def construir_afne_teste() -> AFNe:
    return AFNe(
        estados={"q0", "q1", "q2", "q3", "q4"},
        alfabeto={"a", "b"},
        transicoes={
            ("q0", EPSILON): {"q1"},
            ("q1", "a"): {"q2"},
            ("q2", EPSILON): {"q3"},
            ("q3", "b"): {"q4"},
        },
        inicial="q0",
        finais={"q4"},
    )


def test_epsilon_fecho() -> None:
    afne = construir_afne_teste()
    assert afne.epsilon_fecho({"q0"}) == {"q0", "q1"}
    assert afne.epsilon_fecho({"q2"}) == {"q2", "q3"}


def test_mover() -> None:
    afne = construir_afne_teste()
    assert afne.mover({"q1"}, "a") == {"q2"}
    assert afne.mover({"q3"}, "b") == {"q4"}


def test_aceita() -> None:
    afne = construir_afne_teste()
    assert afne.aceita("ab")
    assert not afne.aceita("")
    assert not afne.aceita("a")
    assert not afne.aceita("b")
    assert not afne.aceita("abc")


def test_simular() -> None:
    historico = construir_afne_teste().simular("ab")
    assert historico[0] == {"q0", "q1"}
    assert historico[1] == {"q2", "q3"}
    assert historico[2] == {"q4"}


def test_simbolo_invalido() -> None:
    with pytest.raises(ValueError):
        construir_afne_teste().mover({"q0"}, "x")


def test_origem_invalida() -> None:
    with pytest.raises(ValueError):
        AFNe(
            estados={"q0", "q1"},
            alfabeto={"a"},
            transicoes={("q9", "a"): {"q1"}},
            inicial="q0",
            finais={"q1"},
        )


def test_destino_invalido() -> None:
    with pytest.raises(ValueError):
        AFNe(
            estados={"q0", "q1"},
            alfabeto={"a"},
            transicoes={("q0", "a"): {"q9"}},
            inicial="q0",
            finais={"q1"},
        )
