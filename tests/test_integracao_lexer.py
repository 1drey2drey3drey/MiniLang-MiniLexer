import subprocess
import sys
from pathlib import Path

import pytest

from src.lexer import LexicalError, format_tokens, tokenize
from src.tokens import TokenType

ROOT = Path(__file__).resolve().parents[1]


def pares(tokens):
    return [(token.type, token.lexeme) for token in tokens]


def tipos(tokens):
    return [token.type for token in tokens]


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        (
            "program if else while print true false",
            [
                (TokenType.PROGRAM, "program"),
                (TokenType.IF, "if"),
                (TokenType.ELSE, "else"),
                (TokenType.WHILE, "while"),
                (TokenType.PRINT, "print"),
                (TokenType.BOOLEAN, "true"),
                (TokenType.BOOLEAN, "false"),
            ],
        ),
        (
            "int float string bool time",
            [
                (TokenType.TYPE_INT, "int"),
                (TokenType.TYPE_FLOAT, "float"),
                (TokenType.TYPE_STRING, "string"),
                (TokenType.TYPE_BOOL, "bool"),
                (TokenType.TYPE_TIME, "time"),
            ],
        ),
    ],
)
def test_todas_as_palavras_reservadas(source, expected):
    assert pares(tokenize(source)) == expected


def test_keyword_e_identificador_sao_case_sensitive():
    tokens = tokenize("int Int true True program Program")
    assert pares(tokens) == [
        (TokenType.TYPE_INT, "int"),
        (TokenType.IDENTIFIER, "Int"),
        (TokenType.BOOLEAN, "true"),
        (TokenType.IDENTIFIER, "True"),
        (TokenType.PROGRAM, "program"),
        (TokenType.IDENTIFIER, "Program"),
    ]


def test_identificadores_com_varios_blocos_de_subunderscore():
    tokens = tokenize("a_b a_b2 valor_total_2 mediaFinal2 nota_final1")
    assert all(token.type is TokenType.IDENTIFIER for token in tokens)
    assert [token.lexeme for token in tokens] == [
        "a_b",
        "a_b2",
        "valor_total_2",
        "mediaFinal2",
        "nota_final1",
    ]


def test_programa_real_completo_gera_sequencia_coerente_de_tokens():
    source = '''program demo {
    int idade = 20;
    float nota = 9.5;
    float fator = 1.5e3;
    string nome = "Andrey";
    bool aprovado = true;
    time entrada = 14:30;
    if (nota >= 7.0) {
        print(nome);
    } else {
        print("Reprovado");
    }
}'''
    tokens = tokenize(source)

    assert pares(tokens) == [
        (TokenType.PROGRAM, "program"),
        (TokenType.IDENTIFIER, "demo"),
        (TokenType.LBRACE, "{"),
        (TokenType.TYPE_INT, "int"),
        (TokenType.IDENTIFIER, "idade"),
        (TokenType.ASSIGN, "="),
        (TokenType.INTEGER, "20"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.TYPE_FLOAT, "float"),
        (TokenType.IDENTIFIER, "nota"),
        (TokenType.ASSIGN, "="),
        (TokenType.DECIMAL, "9.5"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.TYPE_FLOAT, "float"),
        (TokenType.IDENTIFIER, "fator"),
        (TokenType.ASSIGN, "="),
        (TokenType.SCIENTIFIC, "1.5e3"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.TYPE_STRING, "string"),
        (TokenType.IDENTIFIER, "nome"),
        (TokenType.ASSIGN, "="),
        (TokenType.STRING, '"Andrey"'),
        (TokenType.SEMICOLON, ";"),
        (TokenType.TYPE_BOOL, "bool"),
        (TokenType.IDENTIFIER, "aprovado"),
        (TokenType.ASSIGN, "="),
        (TokenType.BOOLEAN, "true"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.TYPE_TIME, "time"),
        (TokenType.IDENTIFIER, "entrada"),
        (TokenType.ASSIGN, "="),
        (TokenType.TIME, "14:30"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.IF, "if"),
        (TokenType.LPAREN, "("),
        (TokenType.IDENTIFIER, "nota"),
        (TokenType.GREATER_EQUAL, ">="),
        (TokenType.DECIMAL, "7.0"),
        (TokenType.RPAREN, ")"),
        (TokenType.LBRACE, "{"),
        (TokenType.PRINT, "print"),
        (TokenType.LPAREN, "("),
        (TokenType.IDENTIFIER, "nome"),
        (TokenType.RPAREN, ")"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.RBRACE, "}"),
        (TokenType.ELSE, "else"),
        (TokenType.LBRACE, "{"),
        (TokenType.PRINT, "print"),
        (TokenType.LPAREN, "("),
        (TokenType.STRING, '"Reprovado"'),
        (TokenType.RPAREN, ")"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.RBRACE, "}"),
        (TokenType.RBRACE, "}"),
    ]


def test_programa_valido_sem_espacos_entre_tokens():
    tokens = tokenize('if(a<=10){print("x");}else{print("y");}')
    assert pares(tokens) == [
        (TokenType.IF, "if"),
        (TokenType.LPAREN, "("),
        (TokenType.IDENTIFIER, "a"),
        (TokenType.LESS_EQUAL, "<="),
        (TokenType.INTEGER, "10"),
        (TokenType.RPAREN, ")"),
        (TokenType.LBRACE, "{"),
        (TokenType.PRINT, "print"),
        (TokenType.LPAREN, "("),
        (TokenType.STRING, '"x"'),
        (TokenType.RPAREN, ")"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.RBRACE, "}"),
        (TokenType.ELSE, "else"),
        (TokenType.LBRACE, "{"),
        (TokenType.PRINT, "print"),
        (TokenType.LPAREN, "("),
        (TokenType.STRING, '"y"'),
        (TokenType.RPAREN, ")"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.RBRACE, "}"),
    ]


def test_operadores_compostos_nao_se_fragmentam():
    tokens = tokenize("a==b!=c<=d>=e")
    assert pares(tokens) == [
        (TokenType.IDENTIFIER, "a"),
        (TokenType.EQUAL, "=="),
        (TokenType.IDENTIFIER, "b"),
        (TokenType.NOT_EQUAL, "!="),
        (TokenType.IDENTIFIER, "c"),
        (TokenType.LESS_EQUAL, "<="),
        (TokenType.IDENTIFIER, "d"),
        (TokenType.GREATER_EQUAL, ">="),
        (TokenType.IDENTIFIER, "e"),
    ]


def test_operadores_simples_adjacentes():
    tokens = tokenize("+ - * / = < >")
    assert tipos(tokens) == [
        TokenType.PLUS,
        TokenType.MINUS,
        TokenType.MULTIPLY,
        TokenType.DIVIDE,
        TokenType.ASSIGN,
        TokenType.LESS,
        TokenType.GREATER,
    ]


def test_minus_nao_faz_parte_do_literal_numerico():
    assert pares(tokenize("-1 - 2.5 - 3e2")) == [
        (TokenType.MINUS, "-"),
        (TokenType.INTEGER, "1"),
        (TokenType.MINUS, "-"),
        (TokenType.DECIMAL, "2.5"),
        (TokenType.MINUS, "-"),
        (TokenType.SCIENTIFIC, "3e2"),
    ]


def test_comentario_no_meio_da_linha_e_no_final():
    source = "int x=1; // primeiro\n// segundo\nprint(x); // final"
    assert pares(tokenize(source)) == [
        (TokenType.TYPE_INT, "int"),
        (TokenType.IDENTIFIER, "x"),
        (TokenType.ASSIGN, "="),
        (TokenType.INTEGER, "1"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.PRINT, "print"),
        (TokenType.LPAREN, "("),
        (TokenType.IDENTIFIER, "x"),
        (TokenType.RPAREN, ")"),
        (TokenType.SEMICOLON, ";"),
    ]


def test_barra_dupla_em_string_nao_inicia_comentario():
    tokens = tokenize('string caminho = "a/b // c";')
    assert pares(tokens) == [
        (TokenType.TYPE_STRING, "string"),
        (TokenType.IDENTIFIER, "caminho"),
        (TokenType.ASSIGN, "="),
        (TokenType.STRING, '"a/b // c"'),
        (TokenType.SEMICOLON, ";"),
    ]


def test_string_contem_todos_os_simbolos_permitidos_da_classe():
    source = '"AZaz09 _.,!?;:+*/=<>-"'
    tokens = tokenize(source)
    assert pares(tokens) == [(TokenType.STRING, source)]


@pytest.mark.parametrize(
    "source",
    [
        "0",
        "1",
        "9",
        "10",
        "999999",
        "0.1",
        "10.0",
        "9.5",
        "1e0",
        "0e1",
        "10e2",
        "1.5e3",
        "9.5E-2",
        "10.25e+4",
        "00:00",
        "09:05",
        "12:30",
        "23:59",
    ],
)
def test_limites_numericos_e_horarios_validos(source):
    tokens = tokenize(source)
    assert len(tokens) == 1


@pytest.mark.parametrize(
    ("source", "message"),
    [
        ("00", "inteiro inválido"),
        ("09.5", "número decimal inválido"),
        ("01e3", "notação científica inválida"),
        ("1e", "notação científica inválida"),
        ("1e+", "notação científica inválida"),
        ("1.5.2", "formato numérico inválido"),
        ("10a", "lexema numérico contaminado"),
        ("1e3a", "lexema numérico contaminado"),
        ("123:45", "formato de horário inválido"),
        ("24:00", "formato de horário inválido"),
        ("12:60", "formato de horário inválido"),
        ("14:30:00", "formato de horário inválido"),
    ],
)
def test_erros_numericos_exibem_motivo(source, message):
    with pytest.raises(LexicalError, match=message):
        tokenize(source)


@pytest.mark.parametrize("source", ["_nome", "nome_", "nome__aluno", "nome__"])
def test_identificadores_invalidos_sao_rejeitados(source):
    with pytest.raises(LexicalError):
        tokenize(source)


def test_identificador_invalido_apos_nova_linha_tem_posicao_correta():
    with pytest.raises(LexicalError) as exc_info:
        tokenize("int x=1;\n\nfoo_ = 2;")
    erro = exc_info.value
    assert erro.line == 3
    assert erro.column == 1
    assert erro.lexeme == "foo_"


def test_simbolo_desconhecido_no_meio_do_programa_preserva_posicao():
    with pytest.raises(LexicalError) as exc_info:
        tokenize("int x = 1;\nfoo = @;")
    erro = exc_info.value
    assert erro.line == 2
    assert erro.column == 7
    assert erro.lexeme == "@"


@pytest.mark.parametrize("source", ["!", "@", ".", ":", "\\", "#"])
def test_simbolos_fora_do_vocabulario_geram_erro(source):
    with pytest.raises(LexicalError):
        tokenize(source)


def test_exclamacao_sozinha_explicita_motivo():
    with pytest.raises(LexicalError, match="operador '!' isolado"):
        tokenize("!")


def test_string_com_tabulacao_e_quebra_de_linha_e_rejeitada():
    for source in ['"a\tb"', '"a\nb"']:
        with pytest.raises(LexicalError, match="string não pode conter tabulação ou quebra de linha"):
            tokenize(source)


def test_string_sem_fechamento_informa_lexema_desde_a_aspa():
    with pytest.raises(LexicalError) as exc_info:
        tokenize('string nome = "Andrey')
    erro = exc_info.value
    assert erro.lexeme == '"Andrey'
    assert erro.column == 15


def test_espacos_tabs_crlf_e_linhas_vazias_mantem_posicoes():
    source = "\r\n\tint\tx=1;\r\n\r\nprint(x);"
    tokens = tokenize(source)
    assert tokens[0].line == 2
    assert tokens[0].column == 2
    assert tokens[1].line == 2
    assert tokens[1].column == 6
    assert tokens[-1].line == 4
    assert tokens[-1].column == 9


def test_format_tokens_vazio_eh_mensagem_controlada():
    assert format_tokens([]) == (
        "Nenhum código foi fornecido.\n\n"
        "A análise léxica não foi realizada."
    )


def test_format_tokens_produz_saida_legivel():
    texto = format_tokens(tokenize("int x=10;"))
    assert 'TYPE_INT' in texto and '"int"' in texto
    assert 'IDENTIFIER     "x"' in texto
    assert 'INTEGER        "10"' in texto
    assert 'SEMICOLON      ";"' in texto


def test_exemplos_do_projeto_tem_comportamento_esperado():
    valido = (ROOT / "examples" / "valido.min").read_text(encoding="utf-8")
    invalido = (ROOT / "examples" / "invalido.min").read_text(encoding="utf-8")

    tokens = tokenize(valido)
    assert tokens[0].type is TokenType.PROGRAM
    assert any(token.type is TokenType.TIME for token in tokens)
    assert any(token.type is TokenType.SCIENTIFIC for token in tokens)
    assert any(token.type is TokenType.STRING for token in tokens)

    with pytest.raises(LexicalError):
        tokenize(invalido)


def test_cli_arquivo_valido_retorna_zero_e_exibe_tokens():
    result = subprocess.run(
        [sys.executable, "-m", "src.main", "examples/valido.min"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "PROGRAM" in result.stdout
    assert "SCIENTIFIC" in result.stdout
    assert "TIME" in result.stdout


def test_cli_arquivo_invalido_retorna_um_e_exibe_diagnostico():
    result = subprocess.run(
        [sys.executable, "-m", "src.main", "examples/invalido.min"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert "ERRO LÉXICO" in result.stdout
    assert "Linha:" in result.stdout
    assert "Coluna:" in result.stdout
    assert "Lexema:" in result.stdout


def test_lexer_nao_produz_tokens_de_comentario():
    tokens = tokenize("// somente comentário")
    assert tokens == []


def test_comentario_no_final_sem_quebra_de_linha_e_ignorado():
    tokens = tokenize("int x=1;//comentário sem newline")
    assert pares(tokens) == [
        (TokenType.TYPE_INT, "int"),
        (TokenType.IDENTIFIER, "x"),
        (TokenType.ASSIGN, "="),
        (TokenType.INTEGER, "1"),
        (TokenType.SEMICOLON, ";"),
    ]


def test_delimitadores_em_programa_real():
    tokens = tokenize("(a,b);{c,d}")
    assert tipos(tokens) == [
        TokenType.LPAREN,
        TokenType.IDENTIFIER,
        TokenType.COMMA,
        TokenType.IDENTIFIER,
        TokenType.RPAREN,
        TokenType.SEMICOLON,
        TokenType.LBRACE,
        TokenType.IDENTIFIER,
        TokenType.COMMA,
        TokenType.IDENTIFIER,
        TokenType.RBRACE,
    ]


@pytest.mark.parametrize("source", ["01", "000", "09", "000.5", "00e1", "000e2", "01.5e2"])
def test_zero_a_esquerda_nunca_e_fragmentado(source):
    with pytest.raises(LexicalError):
        tokenize(source)
