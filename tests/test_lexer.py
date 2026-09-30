import pytest

from src.lexer import LexicalError, tokenize
from src.tokens import TokenType


def types(tokens):
    return [token.type for token in tokens]


def lexemes(tokens):
    return [token.lexeme for token in tokens]


def test_programa_valido_completo():
    source = '''program cadastro {
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
    while (idade < 25) {
        idade = idade + 1;
    }
    // comentário
}'''
    tokens = tokenize(source)
    assert TokenType.PROGRAM in types(tokens)
    assert TokenType.SCIENTIFIC in types(tokens)
    assert TokenType.DECIMAL in types(tokens)
    assert TokenType.STRING in types(tokens)
    assert TokenType.TIME in types(tokens)
    assert TokenType.GREATER_EQUAL in types(tokens)
    assert TokenType.LESS in types(tokens)


def test_keywords_nao_fragmentam_identificador():
    tokens = tokenize("int integer int2 true falsehood")
    assert types(tokens) == [
        TokenType.TYPE_INT,
        TokenType.IDENTIFIER,
        TokenType.IDENTIFIER,
        TokenType.BOOLEAN,
        TokenType.IDENTIFIER,
    ]
    assert lexemes(tokens) == ["int", "integer", "int2", "true", "falsehood"]


def test_operadores_compostos_antes_dos_simples():
    tokens = tokenize("a==b != c <= d >= e < f > g = h")
    assert types(tokens) == [
        TokenType.IDENTIFIER,
        TokenType.EQUAL,
        TokenType.IDENTIFIER,
        TokenType.NOT_EQUAL,
        TokenType.IDENTIFIER,
        TokenType.LESS_EQUAL,
        TokenType.IDENTIFIER,
        TokenType.GREATER_EQUAL,
        TokenType.IDENTIFIER,
        TokenType.LESS,
        TokenType.IDENTIFIER,
        TokenType.GREATER,
        TokenType.IDENTIFIER,
        TokenType.ASSIGN,
        TokenType.IDENTIFIER,
    ]


def test_comentario_nao_vira_divisao():
    tokens = tokenize("a / b // comentario\nc / d")
    assert lexemes(tokens) == ["a", "/", "b", "c", "/", "d"]


def test_numeros_usam_maior_lexema():
    tokens = tokenize("123 9.5 1.5e3 1e3 20:00 20+3 9.5-1")
    assert types(tokens) == [
        TokenType.INTEGER,
        TokenType.DECIMAL,
        TokenType.SCIENTIFIC,
        TokenType.SCIENTIFIC,
        TokenType.TIME,
        TokenType.INTEGER,
        TokenType.PLUS,
        TokenType.INTEGER,
        TokenType.DECIMAL,
        TokenType.MINUS,
        TokenType.INTEGER,
    ]


@pytest.mark.parametrize(
    "source",
    ["007", "09.5", "01e3", "1e", "1e+", "1.5.2", "10a", "1e3a", "123:45", "24:00", "12:60", "14:30:00"],
)
def test_candidatos_invalidos_nao_sao_fragmentados(source):
    with pytest.raises(LexicalError):
        tokenize(source)


def test_string_vazia_e_strings_validas():
    tokens = tokenize('string a = ""; string b = "12:30";')
    assert types(tokens) == [
        TokenType.TYPE_STRING,
        TokenType.IDENTIFIER,
        TokenType.ASSIGN,
        TokenType.STRING,
        TokenType.SEMICOLON,
        TokenType.TYPE_STRING,
        TokenType.IDENTIFIER,
        TokenType.ASSIGN,
        TokenType.STRING,
        TokenType.SEMICOLON,
    ]


def test_string_nao_encerrada():
    with pytest.raises(LexicalError, match="string não encerrada"):
        tokenize('string nome = "Andrey;')


def test_string_nao_permite_tab_e_quebra_de_linha():
    with pytest.raises(LexicalError, match="string não pode conter tabulação ou quebra de linha"):
        tokenize('"linha\n"')


def test_simbolo_desconhecido():
    with pytest.raises(LexicalError, match="símbolo não reconhecido"):
        tokenize("@")


def test_operador_exclamacao_isolado():
    with pytest.raises(LexicalError, match="operador '!' isolado"):
        tokenize("!")


def test_posicao_linha_coluna():
    tokens = tokenize("int x = 1;\nprint(x);")
    assert tokens[0].line == 1 and tokens[0].column == 1
    assert tokens[-1].line == 2 and tokens[-1].column == 9


def test_entrada_vazia():
    assert tokenize("") == []

def test_delimitadores_e_operadores_simples():
    tokens = tokenize("( ) { } ; , + - * / = < >")
    assert types(tokens) == [
        TokenType.LPAREN,
        TokenType.RPAREN,
        TokenType.LBRACE,
        TokenType.RBRACE,
        TokenType.SEMICOLON,
        TokenType.COMMA,
        TokenType.PLUS,
        TokenType.MINUS,
        TokenType.MULTIPLY,
        TokenType.DIVIDE,
        TokenType.ASSIGN,
        TokenType.LESS,
        TokenType.GREATER,
    ]


def test_erro_mantem_posicao_do_inicio_do_lexema():
    with pytest.raises(LexicalError) as exc_info:
        tokenize("  01.5")
    erro = exc_info.value
    assert erro.line == 1
    assert erro.column == 3
    assert erro.lexeme == "01.5"


@pytest.mark.parametrize(
    ("source", "coluna", "lexema"),
    [
        ("x=12abc;", 3, "12abc"),
        ("x = 1a", 5, "1a"),
        ("  7_", 3, "7_"),
    ],
)
def test_inteiro_contaminado_informa_coluna_do_inicio(source, coluna, lexema):
    with pytest.raises(LexicalError) as exc_info:
        tokenize(source)
    erro = exc_info.value
    assert erro.column == coluna
    assert erro.lexeme == lexema


@pytest.mark.parametrize(
    ("source", "motivo"),
    [
        ("1.e5", "deve haver dígitos após o ponto"),
        ("1e", "o expoente deve possuir pelo menos um dígito"),
        ("1.5E+", "o expoente deve possuir pelo menos um dígito"),
        ("01e3", "a parte inteira não pode possuir zero à esquerda"),
    ],
)
def test_cientifico_invalido_informa_motivo_especifico(source, motivo):
    with pytest.raises(LexicalError) as exc_info:
        tokenize(source)
    assert motivo in exc_info.value.message
