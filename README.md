# MiniLexer — analisador léxico da MiniLang

Projeto da disciplina de **Linguagens Formais e Autômatos**. A aplicação implementa um analisador léxico funcional para a linguagem simplificada **MiniLang**, relacionando Expressões Regulares, AFNε de Thompson, testes automatizados e tokenização.

A especificação vigente do projeto está em `MiniLang_Guia_Projeto.md`. Ela deve ser tratada como fonte de verdade para a relação entre linguagem, ER formal, AFNε, regex Python, testes e MiniLexer.

## Requisitos da atividade atendidos

O projeto possui seis Expressões Regulares principais, acima do mínimo de cinco exigido: identificador estruturado, inteiro, decimal, notação científica, string e horário. Para cada ER foram definidos alfabeto, linguagem, ER formal, sintaxe Python, AFNε e casos de teste. A atividade exige, para cada expressão, pelo menos 6 cadeias aceitas, 6 rejeitadas e um ou mais casos-limite.

O enunciado também exige que ER formal, código, testes e AFNε representem a mesma linguagem. Por isso o projeto mantém validação cruzada entre AFNε e `re.fullmatch()` e uma validação estrutural separada das tabelas dos seis AFNε.

## Estrutura

```text
MiniLang-MiniLexer/
├── MiniLang_Guia_Projeto.md      # especificação (fonte de verdade)
├── README.md
├── COMANDOS_APRESENTACAO.md      # roteiro de comandos da demonstração
├── CONTRIBUICOES.md              # registro das contribuições
├── DECLARACAO_IA.md              # declaração de uso de IA
├── requirements.txt
├── pytest.ini
├── src/
│   ├── __init__.py
│   ├── automata.py               # 6 regex + construção Thompson + simulador AFNε
│   ├── patterns.py               # tabelas do lexer (palavras reservadas, operadores)
│   ├── tokens.py
│   ├── lexer.py                  # MiniLexer
│   └── main.py                   # interface de linha de comando
├── tests/
│   ├── conftest.py
│   ├── test_automata.py
│   ├── test_afne_structure.py
│   ├── test_patterns.py
│   ├── test_lexer.py
│   ├── test_examples.py
│   ├── test_integracao_lexer.py
│   ├── validate_afne_structure.py
│   ├── validate_er01.py … validate_er06.py
│   └── validate_all.py
├── docs/
│   ├── apresentacao/
│   │   └── apresentacao.pdf      # slides da apresentação
│   ├── explicacoes/              # ficha explicativa de cada ER (ER-01.md … ER-06.md)
│   ├── diagramas/
│   │   └── ER-01/ … ER-06/
│   │       ├── ER-XX.jff         # AFNε para o JFLAP
│   │       └── ER-XX.md          # AFNε em Mermaid (renderiza no GitHub)
│   └── relatorio/
│       ├── main.tex
│       ├── relatorio_completo.tex
│       ├── relatorio.pdf
│       └── secoes/
└── examples/
    ├── valido.min
    └── invalido.min
```

## MiniLexer

A ordem oficial de tokenização é:

```text
1. whitespace
2. comentário
3. string
4. operador composto
5. científico
6. decimal
7. TIME
8. inteiro
9. identificador / palavra reservada
10. operador simples
11. delimitador
12. erro léxico
```

O lexer preserva prioridade e maior lexema, impedindo que candidatos numéricos inválidos sejam fragmentados silenciosamente. Ele também informa linha, coluna, lexema e motivo do erro.

### Tokens principais

```text
PROGRAM
TYPE_INT TYPE_FLOAT TYPE_STRING TYPE_BOOL TYPE_TIME
IF ELSE WHILE PRINT BOOLEAN
IDENTIFIER INTEGER DECIMAL SCIENTIFIC STRING TIME
PLUS MINUS MULTIPLY DIVIDE
ASSIGN EQUAL NOT_EQUAL LESS GREATER LESS_EQUAL GREATER_EQUAL
LPAREN RPAREN LBRACE RBRACE SEMICOLON COMMA
```

`WHITESPACE` e `COMMENT` são usados internamente e descartados da saída final.

## Execução

Na raiz do projeto:

```bash
python -m src.main examples/valido.min
python -m src.main examples/invalido.min
python -m src.main
```

## Testes

Instale as dependências de teste uma vez (`pip install -r requirements.txt`). Suíte completa:

```bash
pytest
```

Validação de todas as seis ERs:

```bash
python tests/validate_all.py
```

Validação individual:

```bash
python tests/validate_er01.py
python tests/validate_er02.py
python tests/validate_er03.py
python tests/validate_er04.py
python tests/validate_er05.py
python tests/validate_er06.py
```

Validação estrutural exata dos AFNε:

```bash
python tests/validate_afne_structure.py
```

Essa validação compara estados, estado inicial, estados finais, alfabeto, transições, contagens Thompson e a estrutura/rótulos dos arquivos `.jff`. Ela é separada da comparação de linguagem para evitar que dois autômatos diferentes que reconheçam a mesma linguagem sejam considerados estruturalmente iguais.

## Diagramas AFNε

Os seis diagramas estão em `docs/diagramas/`. Cada ER possui somente:

```text
ER-XX.jff   → arquivo para JFLAP
ER-XX.md    → representação Mermaid (renderizada diretamente pelo GitHub)
```

Os dois arquivos são derivados da mesma tabela canônica de transições. Nos `.jff`, cada classe é expandida em transições de um caractere: por exemplo, D corresponde a dez transições, de `0` a `9`. As transições ε usam `<read />`. Os estados e suas posições são preservados; as contagens Thompson da especificação se referem às transições agrupadas, antes dessa expansão.

Os rótulos anteriores, como `[A-Za-z]` e `[0-9]`, produziam resultados incorretos no JFLAP 7.1. Os seis arquivos corrigidos foram carregados e simulados pelo próprio JFLAP 7.1 em **40.044 casos, sem divergências**, incluindo entradas aceitas, rejeitadas, casos-limite, caracteres ASCII e todas as combinações de horário de `00:00` a `99:99`.

Para repetir essa verificação, com JDK 11 ou superior e o arquivo JAR do JFLAP:

```bash
python tests/validate_jflap_runtime.py "C:/Users/igorv/Downloads/JFLAP7.1.jar"
```

Esse comando usa o leitor XML e o simulador do JFLAP sem abrir a interface gráfica. A suíte `pytest` também verifica a linguagem diretamente dos arquivos `.jff`, sem depender do Java.

Para testar pela interface, abra um `.jff` em **File → Open** e use **Input → Multiple Run**. Exemplos: ER-01 aceita `valor_total` e rejeita `nome_`; ER-02 aceita `10` e rejeita `01`; ER-03 aceita `0.5` e rejeita `5.`; ER-04 aceita `1.5e3` e rejeita `1e+`; ER-05 aceita `"abc 123"` (incluindo as aspas) e rejeita `abc`; ER-06 aceita `23:59` e rejeita `24:00`. Consulte também o [tutorial oficial de autômatos do JFLAP](https://www.jflap.org/tutorial/fa/createfa/fa.html).

## Resultados de validação

A validação cruzada registrada para as seis ERs não encontrou divergências nas baterias e alfabetos reduzidos definidos na especificação. A validação estrutural dos seis AFNε também está integrada à suíte de testes.

Os testes exaustivos com alfabetos reduzidos verificam o espaço de cadeias efetivamente escolhido para cada ER; eles não são uma afirmação de teste de todos os alfabetos possíveis da linguagem.

## Limitações atuais

O projeto é exclusivamente léxico. O MiniLexer interrompe a análise no primeiro erro léxico encontrado (não há recuperação de erros), por isso `examples/invalido.min` exibe apenas o primeiro erro do arquivo. Não possui análise sintática, semântica, compilação ou execução da MiniLang. A regra de strings não possui escapes na primeira versão. A validação dos números verifica formato lexical, não interpretação matemática.

## Dependências

O único pacote externo de desenvolvimento atualmente listado é o `pytest`. A aplicação usa a biblioteca padrão do Python.

Instalação:

```bash
pip install -r requirements.txt
```

## Uso de Inteligência Artificial

O projeto utilizou IA (Claude e ChatGPT) como apoio em análise da especificação, Expressões Regulares, construção e validação de AFNε, implementação do MiniLexer, testes, diagramas e documentação. O uso, as tarefas apoiadas e a responsabilidade da equipe estão registrados em `DECLARACAO_IA.md`.

## Registro de contribuições

As contribuições da equipe estão registradas em `CONTRIBUICOES.md`:

- **Andrey Lourival Andrade Garcia** — especificação da MiniLang, AFNε, simulador, MiniLexer, testes, diagramas e documentação;
- **Igor Cecim Vilhena** — Expressões Regulares, relatório técnico e slides.

## Relatório técnico

O relatório técnico está em `docs/relatorio/`. O arquivo `main.tex` é o documento principal para edição no Overleaf; `relatorio_completo.tex` é a versão consolidada em um único arquivo e `relatorio.pdf` é a versão compilada incluída no pacote.

## Apresentação

Os slides da apresentação estão em `docs/apresentacao/apresentacao.pdf`.

## Estado atual

```text
✓ especificação MiniLang
✓ seis ERs formais
✓ seis AFNε
✓ simulador AFNε
✓ validação AFNε × regex
✓ validação estrutural dos AFNε
✓ MiniLexer
✓ testes unitários e integrados
✓ exemplos .min
✓ diagramas JFLAP + Mermaid
✓ README atualizado
✓ declaração de uso de IA
✓ registro de contribuições criado
✓ contribuições registradas
✓ relatório técnico em LaTeX + PDF
✓ apresentação
→ ensaio final
```
