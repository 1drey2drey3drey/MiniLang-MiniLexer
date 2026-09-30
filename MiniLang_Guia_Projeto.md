# MiniLang — Guia Base e Especificação do Projeto

> **Versão:** 4.5 — consolidação da implementação do MiniLexer  
> **Data:** 30/09/2026  
> **Disciplina:** Linguagens Formais e Autômatos  
> **Projeto:** MiniLexer — Analisador Léxico da MiniLang  
> **Status:** especificação consolidada; seis AFNε implementados e validados; MiniLexer funcional; suíte integrada ampliada e validada

---

## 0. Regra principal deste documento

Este arquivo é a **fonte de verdade vigente da MiniLang**.

Toda decisão estrutural da linguagem deverá aparecer aqui antes de ser implementada.

A cadeia de consistência do projeto é:

```text
ESPECIFICAÇÃO DA MINILANG
        ↓
LINGUAGEM L
        ↓
ER FORMAL
        ↓
AFNε
        ↓
REGEX NO CÓDIGO
        ↓
TESTES
        ↓
COMPORTAMENTO DO MINILEXER
```

Se uma regra for alterada, todos os elementos dependentes deverão ser revisados.

A expressão formal, a sintaxe do código, os testes e o AFNε devem reconhecer a mesma linguagem.

---

# 1. Base utilizada

A especificação deste projeto foi construída considerando o enunciado da atividade e o guia fornecido pelo professor.

Os pontos especialmente relevantes são:

- aplicação funcional com entradas, processamento e saídas;
- mínimo de cinco Expressões Regulares relevantes;
- tratamento de entradas vazias e inválidas;
- mensagens claras;
- código organizado;
- para cada ER: alfabeto, linguagem, ER formal, sintaxe do código, equivalência, AFNε e testes;
- mínimo de seis cadeias aceitas e seis rejeitadas por ER;
- pelo menos um caso-limite;
- equivalência entre ER formal, código, testes e AFNε;
- possibilidade de o professor solicitar novos dados durante a apresentação.

O guia também estabelece a distinção entre a representação formal da linguagem e a sintaxe efetivamente utilizada pelo motor de Expressões Regulares da linguagem de programação.

---

# 2. Revisões feitas nesta versão

Esta especificação consolida as decisões formais e de implementação das seis Expressões Regulares, dos AFNε e do MiniLexer. As decisões abaixo foram congeladas antes da implementação e permanecem vigentes.

## 2.1 ER-01 — identificador estruturado

A ER própria da MiniLang é:

\[
L(A\mid\_AA^*)^*
\]

com `L` para letras, `D` para dígitos e `A=L∪D` como classe alfanumérica. O sublinhado só pode aparecer como separador interno e deve ser seguido por pelo menos um símbolo alfanumérico.

Durante a auditoria intermediária, uma contagem de **22 estados, 28 transições, 22 transições ε e 6 transições rotuladas** foi registrada. Essa contagem foi posteriormente descartada e não faz parte da especificação vigente. A contagem definitiva da ER-01 é **28 estados, 35 transições, 27 ε e 8 rotuladas**, conforme a construção registrada na seção 9.9.

### 2.1.1 ER-01 — construção Thompson e simulação auditadas

A construção foi rederivada de acordo com a ER formal:

```text
A = L | D
A*
_AA*
L | _AA*
(L | _AA*)*
```

Com a letra inicial `L` fora do Kleene externo, a estrutura completa é equivalente a:

```text
L (A | _AA*)*
```

A construção Thompson definitiva possui:

- `Q = {q0, ..., q27}`;
- estado inicial `q0`;
- estado final `q27`;
- **28 estados**;
- **35 transições**;
- **27 transições ε**;
- **8 transições rotuladas**.

As oito transições rotuladas correspondem à letra inicial, às quatro ocorrências rotuladas das duas construções de `A`, ao `_` e às duas ocorrências rotuladas do `A*`.

#### Simulação formal registrada

A simulação usa repetidamente:

`ε-fecho → move(símbolo) → ε-fecho`.

Casos verificados:

| Cadeia | Resultado | Justificativa |
|---|---|---|
| `a` | aceita | menor identificador válido |
| `abc` | aceita | sequência de letras válida |
| `a1` | aceita | `A` permite dígito após a letra inicial |
| `a_b` | aceita | `_` inicia bloco seguido de alfanumérico |
| `a_b2` | aceita | bloco iniciado por `_` seguido de alfanuméricos |
| `ε` | rejeita | a letra inicial é obrigatória |
| `_a1` | rejeita | identificador não pode começar por `_` |
| `abc_` | rejeita | `_` precisa ser seguido por `A` |
| `a__b` | rejeita | `_` não pode ser seguido diretamente por `_` |
| `1a` | rejeita | identificador não pode começar por dígito |

A tabela do AFNε foi validada por simulação e coincide com a linguagem da ER formal nos casos de teste acima.

## 2.2 ER-02 — inteiro sem zero à esquerda

A regra definitiva é:

\[
L_{INT}=\{0\}\cup ND^*
\]

A construção de Thompson definitiva foi reconstruída e validada. Possui **10 estados, 12 transições, 9 transições ε e 3 transições rotuladas**.

### 2.2.1 ER-02 — AFNε definitivo

A ER-02 é:

\[
L_{INT}=0\mid ND^*
\]

com `N=[1-9]` e `D=[0-9]`. A convenção Thompson utiliza `q0` como estado inicial e `q1` como estado final.

| # | Origem | Símbolo | Destino | Tipo |
|---:|---|---|---|---|
| 1 | q0 | ε | q2 | ε |
| 2 | q0 | ε | q4 | ε |
| 3 | q2 | `0` | q3 | rotulada |
| 4 | q3 | ε | q1 | ε |
| 5 | q4 | `N` | q5 | rotulada |
| 6 | q5 | ε | q8 | ε |
| 7 | q8 | ε | q6 | ε |
| 8 | q8 | ε | q9 | ε |
| 9 | q6 | `D` | q7 | rotulada |
| 10 | q7 | ε | q6 | ε |
| 11 | q7 | ε | q9 | ε |
| 12 | q9 | ε | q1 | ε |

Contagem: `10 estados / 12 transições / 9 ε / 3 rotuladas`, com `9 + 3 = 12`.

### 2.2.2 ER-02 — simulação e validação cruzada

Foram verificados os casos de aceitação e rejeição do AFNε, incluindo fronteiras de zero à esquerda.

| Cadeia | AFNε | Regex de referência | Resultado |
|---|---|---|---|
| `0` | aceita | aceita | ✓ |
| `1` | aceita | aceita | ✓ |
| `7` | aceita | aceita | ✓ |
| `9` | aceita | aceita | ✓ |
| `10` | aceita | aceita | ✓ |
| `20` | aceita | aceita | ✓ |
| `2026` | aceita | aceita | ✓ |
| `999` | aceita | aceita | ✓ |
| `ε` | rejeita | rejeita | ✓ |
| `00` | rejeita | rejeita | ✓ |
| `01` | rejeita | rejeita | ✓ |
| `007` | rejeita | rejeita | ✓ |
| `0123` | rejeita | rejeita | ✓ |
| `-1` | rejeita | rejeita | ✓ |
| `1.5` | rejeita | rejeita | ✓ |

Resultado: **15/15 casos coincidem** entre AFNε e expressão regular de referência. A ER-02 fica teoricamente validada para os casos documentados.

Casos de fronteira adicionais a manter na implementação: `000`, `09`, `100`, `1a`, `10a`, `123.` e `123_`.

## 2.3 ER-03 — decimal

Para evitar a ambiguidade do ponto, definimos:

\[
P=\{\texttt{.}\}
\]

e usamos:

\[
(0\mid ND^*)PDD^*
\]

No código, o ponto é representado por `\.`.

## 2.4 ER-04 — notação científica

A expressão científica definitiva é:

\[
(0\mid ND^*)(PDD^*\mid\varepsilon)(e\mid E)(+\mid-\mid\varepsilon)DD^*
\]

A auditoria corrigiu uma contagem anterior: a construção canônica de Thompson possui **42 estados, 52 transições, 40 transições ε e 12 transições rotuladas**.

A contagem 38/47/36/11 está obsoleta e não deve ser utilizada.

## 2.5 ER-05 — string

A linguagem continua sendo:

\[
L_{STR}=\{\texttt{"}x\texttt{"}\mid x\in C^*\}
\]

A string vazia é válida. Não existem escapes na primeira versão, e `\`, tabulação e quebra de linha não pertencem ao conjunto `C`.



## 2.X ER-05 — validação cruzada AFNε × regex

A ER-05 foi submetida à validação cruzada entre o AFNε de Thompson e a regex Python de referência:

```python
r'"[A-Za-z0-9 _.,!?;:+*/=<>-]*"'
```

### Bateria oficial

Foram comparadas 12 cadeias:

- 6 aceitas;
- 6 rejeitadas.

Resultado:

\[
\boxed{12/12\text{ coincidências}}
\]

### Casos de fronteira

Também foram comparados 6 casos adicionais, cobrindo:

- caracteres permitidos;
- operadores;
- conteúdo unitário;
- tabulação;
- quebra de linha;
- caracteres fora de `C`.

Resultado:

\[
\boxed{6/6\text{ coincidências}}
\]

### Teste exaustivo limitado

Foi realizada uma comparação exaustiva para todas as cadeias de tamanho 0 até 5 sobre um alfabeto reduzido de teste.

Total:

\[
\boxed{177.156\text{ cadeias}}
\]

Divergências encontradas:

\[
\boxed{0}
\]

Portanto, dentro da bateria oficial, dos casos de fronteira e do espaço exaustivo testado:

\[
\boxed{AFN_{\varepsilon,05}(s)=Regex_{05}(s)}
\]

A ER-05 está validada e congelada.

### Estado da ER-05

| Item | Estado |
|---|---|
| ER formal | ✓ |
| Regex Python | ✓ |
| AFNε | ✓ |
| 8 estados | ✓ |
| 9 transições | ✓ |
| 6 ε | ✓ |
| 3 rotuladas | ✓ |
| Simulação | ✓ |
| 6 aceitas + 6 rejeitadas | ✓ |
| Validação cruzada | ✓ |
| Casos de fronteira | ✓ |
| Teste exaustivo limitado | ✓ |
| Divergências | 0 |
| Implementação do lexer | ✓ |


## 2.6 ER-06 — horário

A linguagem definitiva reconhece `HH:MM`, com `00–23` para a hora e `00–59` para minutos. Para o separador definimos:

\[
Q=\{\texttt{:}\}
\]

A construção definitiva possui **16 estados, 16 transições e 9 transições ε** quando as classes são apresentadas como rótulos agrupados.

## 2.7 Convenção Thompson congelada

Todos os seis AFNε usarão a mesma convenção:

- átomo: 2 estados e 1 transição;
- concatenação: ligação por 1 transição ε;
- união: novo início e novo fim com transições ε;
- `*`: novo início e novo fim com ciclo por ε;
- classes finitas: rótulos agrupados no diagrama, com expansão por símbolo apenas quando necessária.

Nenhuma ER será implementada antes de sua forma formal, código, AFNε e testes estarem alinhados.


# 3. Identificação do projeto

## 3.1 Nome da linguagem

**MiniLang**

## 3.2 Nome da aplicação

**MiniLexer**

## 3.3 Tipo

Analisador Léxico de uma linguagem de programação simplificada.

## 3.4 Problema

O usuário fornece um código-fonte escrito em MiniLang.

O MiniLexer identifica os lexemas e os classifica como tokens, além de informar erros léxicos.

Fluxo:

```text
CÓDIGO MINILANG
      ↓
LEITURA
      ↓
ANÁLISE LÉXICA
      ↓
RECONHECIMENTO DOS PADRÕES
      ↓
CLASSIFICAÇÃO DOS LEXEMAS
      ↓
TOKENS
```

---

# 4. Objetivo acadêmico

O objetivo do projeto é relacionar a teoria de Linguagens Formais e Autômatos com uma aplicação concreta.

Para as Expressões Regulares principais, serão demonstrados:

```text
alfabeto
↓
linguagem
↓
ER formal
↓
AFNε
↓
ER no código
↓
testes
```

A aplicação servirá como demonstração prática de reconhecimento de linguagens regulares.

---

# 5. Escopo da MiniLang

A MiniLang possuirá:

- programas;
- variáveis;
- tipos inteiros;
- tipos decimais;
- strings;
- booleanos;
- identificadores;
- horário;
- condicionais;
- repetição;
- impressão;
- operadores;
- delimitadores;
- comentários.

O projeto é **léxico**.

Não haverá:

- compilação;
- execução;
- análise semântica;
- verificação completa de tipos;
- geração de código;
- máquina virtual.

---

# 6. Alfabeto geral

O alfabeto geral da MiniLang inclui os símbolos necessários para sua especificação atual.

## 6.1 Letras

```text
A-Z
a-z
```

## 6.2 Dígitos

```text
0-9
```

## 6.3 Sublinhado

```text
_
```

## 6.4 Operadores

```text
+
-
*
/
=
!
<
>
```

## 6.5 Delimitadores

```text
(
)
{
}
;
,
```

## 6.6 Ponto

```text
.
```

O ponto não é um token isolado da MiniLang.

Ele é utilizado na formação de números decimais e científicos.

Um `.` isolado gera erro léxico.

## 6.7 Outros caracteres

```text
"
espaço
tabulação
quebra de linha
```

A presença de um caractere fora do conjunto admitido e fora das regras de cada ER deve resultar em erro léxico.

---

# 7. Palavras reservadas

A MiniLang possui as seguintes palavras reservadas:

```text
program
int
float
string
bool
time
if
else
while
print
true
false
```

## 7.1 Tabela

| Lexema | Token | Função |
|---|---|---|
| `program` | PROGRAM | Início do programa |
| `int` | TYPE_INT | Tipo inteiro |
| `float` | TYPE_FLOAT | Tipo decimal |
| `string` | TYPE_STRING | Tipo textual |
| `bool` | TYPE_BOOL | Tipo booleano |
| `time` | TYPE_TIME | Tipo horário |
| `if` | IF | Condicional |
| `else` | ELSE | Alternativa |
| `while` | WHILE | Repetição |
| `print` | PRINT | Impressão |
| `true` | BOOLEAN | Valor verdadeiro |
| `false` | BOOLEAN | Valor falso |

### Decisão

Palavras reservadas serão reconhecidas por **tabela de palavras reservadas**, não como uma das ERs principais avaliadas.

Isso evita gastar uma das cinco ou mais ERs obrigatórias em uma simples união finita de palavras.

---

# 8. Identificadores

## 8.1 Regra

Um identificador:

1. começa obrigatoriamente com uma letra;
2. pode continuar com letras e dígitos;
3. pode conter `_` somente como separador interno;
4. `_` não pode ser o último caractere;
5. `__` não é permitido.

### Aceitos

```text
a
nome
idade
aluno1
valor_total
mediaFinal2
nota_final1
a_b
```

### Rejeitados

```text
1aluno
2idade
_nome
nome_
nome__aluno
nome-aluno
nome.aluno
123
```

---

# 9. ER-01 — Identificador estruturado

## 9.1 Finalidade

Reconhecer identificadores válidos da MiniLang.

A regra da MiniLang é própria do projeto e não copia o padrão ilustrativo apresentado na lauda do professor.

Um identificador:

- começa obrigatoriamente com uma letra;
- pode continuar com letras ou dígitos;
- pode usar `_` como separador interno;
- `_` precisa ser seguido por pelo menos um caractere alfanumérico;
- não pode terminar com `_`;
- não pode possuir dois `_` consecutivos.

---

## 9.2 Exemplos

### Aceitos

```text
a
nome
idade
aluno1
valor_total
mediaFinal2
nota_final1
a_b
a1_b2
```

### Rejeitados

```text
1aluno
2idade
_nome
nome_
nome__aluno
nome__
123
nome-aluno
nome.aluno
```

---

## 9.3 Conjuntos auxiliares

Definimos:

\[
L=\{A,\ldots,Z,a,\ldots,z\}
\]

Conjunto das letras.

\[
D=\{0,1,\ldots,9\}
\]

Conjunto dos dígitos.

Também utilizaremos:

\[
A=L\cup D
\]

Assim, `A` representa um caractere alfanumérico.

---

## 9.4 Alfabeto

\[
\boxed{\Sigma_{ID}=L\cup D\cup\{\_\}}
\]

---

## 9.5 Linguagem reconhecida

A linguagem possui a estrutura:

```text
LETRA
seguida de zero ou mais blocos:
    ALFANUMÉRICO
    OU
    _ + ALFANUMÉRICO + ALFANUMÉRICOS*
```

Formalmente:

\[
L_{ID}=\left\{x_1x_2\ldots x_n\mid x_1\in L,\; x_i\in L\cup D\cup\{\_\},\;\text{e cada `_` é seguido por ao menos um alfanumérico}\right\}
\]

A regra específica sobre `_` impede identificadores como:

```text
valor_
valor__total
```

---

## 9.6 ER formal

A expressão regular formal escolhida é:

\[
\boxed{
L\left(A\mid\_AA^*\right)^*
}
\]

Como:

\[
A=L\cup D
\]

podemos expandir:

\[
\boxed{
L\left((L\cup D)\mid\_(L\cup D)(L\cup D)^*\right)^*
}
\]

### Interpretação

Primeiro:

\[
L
\]

exige uma letra inicial.

Depois:

\[
\left(A\mid\_AA^*\right)^*
\]

permite repetir blocos de duas formas:

1. um único caractere alfanumérico;
2. `_` seguido por um ou mais caracteres alfanuméricos.

A lauda estabelece que repetição, concatenação e união devem ser explicitadas e que a precedência deve ser respeitada. fileciteturn1file0L33-L49

---

## 9.7 Sintaxe implementada em Python

```python
r"[A-Za-z]([A-Za-z0-9]|_[A-Za-z0-9]+)*"
```

Para validar a cadeia completa:

```python
re.fullmatch(
    r"[A-Za-z]([A-Za-z0-9]|_[A-Za-z0-9]+)*",
    cadeia
)
```

O guia recomenda `re.fullmatch()` em Python para correspondência completa. fileciteturn1file1L83-L96

---

## 9.8 Equivalência formal × Python

| Representação formal | Sintaxe Python |
|---|---|
| `L` | `[A-Za-z]` |
| `A = L ∪ D` | `[A-Za-z0-9]` |
| `A*` | `[A-Za-z0-9]*` |
| `_` | `_` |
| `_AA*` | `_[A-Za-z0-9]+` |
| união `\mid` | `|` |
| agrupamento | `( ... )` |
| fecho `*` | `*` |

No trecho:

```python
_[A-Za-z0-9]+
```

usamos `+` para representar uma ou mais ocorrências de `A`. Pela equivalência apresentada na lauda:

\[
A^+=AA^*
\]

A lauda define explicitamente `+` como fecho positivo e `?` como opcionalidade. fileciteturn1file0L33-L49

---

# 9.9 AFNε — Construção de Thompson

## 9.9.1 Convenção

O AFNε é derivado diretamente da ER formal:

\[
L(A\mid\_AA^*)^*
\]

com:

- `L = [A-Za-z]`
- `D = [0-9]`
- `A = L | D`

A leitura estrutural é `L` inicial seguido de zero ou mais ocorrências do bloco `A | _AA*`. Portanto, depois da primeira letra, dígitos e letras podem aparecer diretamente, e um `_` só pode iniciar um bloco seguido de pelo menos um caractere alfanumérico.

`L`, `D` e `A` são abreviações de conjuntos/expressões, não símbolos adicionais do alfabeto.

A construção usa Thompson clássico: união e Kleene recebem seus estados auxiliares próprios; concatenação é feita por ε-transições.

## 9.9.2 Estados e contagem

\[
Q=\{q_0,q_1,\ldots,q_{27}\}
\]

Estado inicial: `q0`  
Estado final: `q27`

A contagem correta, obtida pela construção Thompson literal da ER completa, é:

\[
\boxed{28\text{ estados},\;35\text{ transições},\;27\varepsilon,\;8\text{ rotuladas}}
\]

As versões anteriores `16/20/15/5`, `22/28/22/6` e `24/30/23/7` estão obsoletas e não devem ser usadas.

## 9.9.3 Tabela definitiva

| # | Origem | Símbolo | Destino | Tipo |
|---:|---|---|---|---|
| 1 | `q0` | `L` | `q1` | rotulada |
| 2 | `q1` | `ε` | `q26` | ε |
| 3 | `q6` | `ε` | `q2` | ε |
| 4 | `q6` | `ε` | `q4` | ε |
| 5 | `q2` | `L` | `q3` | rotulada |
| 6 | `q3` | `ε` | `q7` | ε |
| 7 | `q4` | `D` | `q5` | rotulada |
| 8 | `q5` | `ε` | `q7` | ε |
| 9 | `q8` | `_` | `q9` | rotulada |
| 10 | `q9` | `ε` | `q14` | ε |
| 11 | `q14` | `ε` | `q10` | ε |
| 12 | `q14` | `ε` | `q12` | ε |
| 13 | `q10` | `L` | `q11` | rotulada |
| 14 | `q11` | `ε` | `q15` | ε |
| 15 | `q12` | `D` | `q13` | rotulada |
| 16 | `q13` | `ε` | `q15` | ε |
| 17 | `q15` | `ε` | `q16` | ε |
| 18 | `q16` | `ε` | `q18` | ε |
| 19 | `q16` | `ε` | `q17` | ε |
| 20 | `q18` | `ε` | `q20` | ε |
| 21 | `q18` | `ε` | `q22` | ε |
| 22 | `q20` | `L` | `q21` | rotulada |
| 23 | `q22` | `D` | `q23` | rotulada |
| 24 | `q21` | `ε` | `q19` | ε |
| 25 | `q23` | `ε` | `q19` | ε |
| 26 | `q19` | `ε` | `q18` | ε |
| 27 | `q19` | `ε` | `q17` | ε |
| 28 | `q24` | `ε` | `q6` | ε |
| 29 | `q24` | `ε` | `q8` | ε |
| 30 | `q7` | `ε` | `q25` | ε |
| 31 | `q17` | `ε` | `q25` | ε |
| 32 | `q26` | `ε` | `q24` | ε |
| 33 | `q26` | `ε` | `q27` | ε |
| 34 | `q25` | `ε` | `q24` | ε |
| 35 | `q25` | `ε` | `q27` | ε |

## 9.9.4 Validação da construção

A tabela é organizada em quatro partes:

1. `q0 --L--> q1`: primeira letra obrigatória;
2. `q6...q7`: `A = L | D` do ramo simples do bloco repetível;
3. `q8...q19`: `_AA*`, em que `_` é seguido obrigatoriamente por um `A` e depois por zero ou mais `A`;
4. `q18...q19`: união `A | _AA*`, seguida do Kleene externo `q24...q25`.

Consequentemente:

- `a` → aceita;
- `abc` → aceita;
- `a1` → aceita;
- `a_b` → aceita;
- `a_b2` → aceita;
- `_a1` → rejeita;
- `abc_` → rejeita;
- `a__b` → rejeita;
- `1a` → rejeita;
- `ε` → rejeita.

A tabela contém exatamente:

\[
28\text{ estados},\quad35\text{ transições},\quad27\varepsilon,\quad8\text{ rotuladas}.
\]

# 9.10 Testes

O enunciado exige no mínimo seis cadeias aceitas, seis rejeitadas e pelo menos um caso-limite. fileciteturn1file2

## Aceitas

| # | Cadeia | Justificativa |
|---|---|---|
| 1 | `a` | menor identificador válido |
| 2 | `nome` | somente letras |
| 3 | `aluno1` | letras e dígitos |
| 4 | `valor_total` | `_` interno válido |
| 5 | `mediaFinal2` | letras e dígitos |
| 6 | `a1_b2` | `_` interno com conteúdo alfanumérico dos dois lados |

## Rejeitadas

| # | Cadeia | Justificativa |
|---|---|---|
| 1 | `ε` | cadeia vazia |
| 2 | `1aluno` | começa com dígito |
| 3 | `_nome` | começa com `_` |
| 4 | `nome_` | termina com `_` |
| 5 | `nome__aluno` | dois `_` consecutivos |
| 6 | `nome-aluno` | `-` não pertence ao padrão |

## Casos-limite

### Caso-limite positivo

```text
a
```

É o identificador válido de menor comprimento.

### Caso-limite negativo

```text
ε
```

A cadeia vazia é rejeitada porque a expressão exige uma letra inicial.

### Caso-limite estrutural

```text
a_
```

Rejeitado porque `_` não pode ser o último símbolo.

### Outro caso-limite estrutural

```text
a__b
```

Rejeitado porque `_` deve ser seguido imediatamente por um caractere alfanumérico.

---

# 9.11 Observação sobre palavras reservadas

Lexemas como:

```text
int
float
string
bool
program
```

possuem formato compatível com a ER de identificadores.

A classificação final será feita pelo lexer:

```text
lexema completo
      ↓
formato de identificador?
      ↓
sim
      ↓
tabela de palavras reservadas
      ├── encontrado → TOKEN RESERVADO
      └── não encontrado → IDENTIFIER
```

Assim:

```text
int       → TYPE_INT
integer   → IDENTIFIER
```

Isso é uma regra de **classificação léxica**, não uma alteração da linguagem matemática de `L_ID`.

---

# 9.12 Resultado e limitações

A ER-01 reconhece a forma dos identificadores, mas não verifica:

- se o identificador foi declarado;
- se existe outra variável com o mesmo nome;
- se o nome é permitido semanticamente em determinado contexto;
- se o identificador representa variável, programa ou outra entidade.

Esses aspectos não fazem parte da análise léxica.

---

# 9.13 Estado da ER-01

```text
✓ finalidade
✓ alfabeto
✓ linguagem
✓ ER formal
✓ sintaxe Python
✓ equivalência formal × código
✓ AFNε de Thompson
✓ estados numerados
✓ transições
✓ transições ε
✓ simulação de cadeia aceita
✓ simulação de cadeia rejeitada
✓ 6 aceitas
✓ 6 rejeitadas
✓ casos-limite
✓ limitações
```

A ER-01 pode agora ser considerada **formalmente fechada**, permanecendo apenas a preparação do diagrama gráfico final para os materiais de apresentação.

---

# 10. Números inteiros

## 10.1 Regra

Um inteiro da MiniLang será: `0` ou um dígito de `1` a `9` seguido por zero ou mais dígitos. A regra proíbe zeros à esquerda nos inteiros com mais de um dígito.

### Aceitos

```text
0
1
7
10
20
2026
999999
```

### Rejeitados

```text
00
01
007
0123
-10
12.5
10a
```

O sinal negativo será reconhecido separadamente como `MINUS`.

---

# 11. ER-02 — Inteiro sem zero à esquerda

## 11.1 Conjuntos

Definimos:

\[ D=\{0,1,\ldots,9\} \]

\[ N=\{1,2,\ldots,9\} \]

## 11.2 Alfabeto

\[ \boxed{\Sigma_{INT}=D} \]

## 11.3 Linguagem

A linguagem dos inteiros é:

\[ \boxed{L_{INT}=\{0\}\cup ND^*} \]

Em palavras: a cadeia é exatamente `0`, ou começa com um dígito de `1` a `9` e continua com zero ou mais dígitos.

Consequentemente:

```text
0       → aceita
8       → aceita
10      → aceita
2026    → aceita

00      → rejeita
01      → rejeita
007     → rejeita
```

A cadeia vazia é rejeitada:

\[ \varepsilon\notin L_{INT} \]

## 11.4 ER formal

\[ \boxed{0\mid ND^*} \]

A primeira alternativa `0` reconhece somente o inteiro zero.

A segunda alternativa `ND*` reconhece um dígito entre `1` e `9`, seguido de zero ou mais dígitos.

O `*` permite que a parte complementar tenha zero ou mais ocorrências. Por isso `7` é válido, enquanto `07` não é.

## 11.5 Sintaxe Python

```python
r"(0|[1-9][0-9]*)"
```

Correspondência completa:

```python
re.fullmatch(r"(0|[1-9][0-9]*)", cadeia)
```

O padrão será utilizado sobre a cadeia inteira, conforme a orientação do guia para correspondência completa.

## 11.6 Equivalência formal × Python

| Formal | Python |
|---|---|
| `0` | `0` |
| `N` | `[1-9]` |
| `D` | `[0-9]` |
| `D*` | `[0-9]*` |
| união `|` | `|` |
| concatenação | justaposição |
| agrupamento | `( ... )` |

Assim:

\[ 0\mid ND^* \]

corresponde a:

```text
(0|[1-9][0-9]*)
```

As classes `[1-9]` e `[0-9]` são atalhos computacionais para uniões finitas de símbolos.

## 11.7 AFNε — Construção de Thompson

O AFNε definitivo corresponde a:

\[
0\mid ND^*
\]

Estados:

\[
Q=\{q_0, q_1, q_2, q_3, q_4, q_5, q_6, q_7, q_8, q_9\}
\]

Estado inicial: `q0`  
Estado final: `q1`

\[
\boxed{10\text{ estados},\;12\text{ transições},\;9\varepsilon,\;3\text{ rotuladas}}
\]

### Tabela definitiva

| Origem | Símbolo | Destino |
|---|---|---|
| `q2` | `0` | `q3` |
| `q0` | `ε` | `q2` |
| `q3` | `ε` | `q1` |
| `q4` | `N` | `q5` |
| `q8` | `D` | `q9` |
| `q6` | `ε` | `q8` |
| `q6` | `ε` | `q7` |
| `q9` | `ε` | `q8` |
| `q9` | `ε` | `q7` |
| `q5` | `ε` | `q6` |
| `q0` | `ε` | `q4` |
| `q7` | `ε` | `q1` |

A contagem definitiva possui **9 transições ε**.

## 11.8 Simulação — cadeia aceita

Cadeia:

```text
2026
```

Percurso principal:

```text
q0 --ε--> q4
q4 --2--> q5
q5 --ε--> q8
q8 --ε--> q6
q6 --0--> q7
q7 --ε--> q6
q6 --2--> q7
q7 --ε--> q6
q6 --6--> q7
q7 --ε--> q9
q9 --ε--> q1
```

A entrada termina em `q1`, que é final.

\[ \boxed{2026\text{ é aceita}} \]

## 11.9 Simulação — cadeia rejeitada

Cadeia:

```text
007
```

No ramo `0`, o autômato consome apenas o primeiro `0` e chega a `q1`, mas a entrada ainda possui `07`. Esse ramo não consegue consumir o restante.

No ramo `ND*`, o primeiro símbolo também não é aceito porque `0` não pertence a `N={1,...,9}`.

Logo:

\[ \boxed{007\text{ é rejeitada}} \]

## 11.10 Testes obrigatórios

### Aceitas

| # | Cadeia | Motivo |
|---|---|---|
| 1 | `0` | Alternativa `0` |
| 2 | `1` | `N` + zero `D` |
| 3 | `7` | `N` + zero `D` |
| 4 | `10` | `N D` |
| 5 | `2026` | `N D*` |
| 6 | `999999` | `N` + vários `D` |

### Rejeitadas

| # | Cadeia | Motivo |
|---|---|---|
| 1 | `ε` | cadeia vazia |
| 2 | `00` | zero não pode possuir continuação |
| 3 | `01` | zero à esquerda |
| 4 | `007` | zero à esquerda |
| 5 | `12.5` | possui `.` |
| 6 | `-10` | `-` é operador separado |

### Casos-limite

```text
0   → menor inteiro permitido
1   → menor inteiro positivo
00  → menor caso inválido por zero à esquerda
01  → zero à esquerda seguido de dígito válido
ε   → menor cadeia possível, mas inválida
```

## 11.11 Limitações e decisões

- Números negativos não pertencem à ER-02; o sinal será token `MINUS`.
- Zeros à esquerda são proibidos por decisão da especificação.
- A ER verifica apenas a forma lexical, não o valor matemático.
- `10` pertence à ER-02; `10.5` deverá pertencer à ER-03.
- No lexer, números decimais e científicos terão prioridade sobre inteiros para impedir a fragmentação de lexemas.

---

# 12. Números decimais

Um decimal possuirá:

```text
parte inteira válida
+
.
+
um ou mais dígitos
```

### Aceitos

```text
0.5
0.50
1.5
9.5
10.25
2026.75
```

### Rejeitados

```text
00.5
01.5
.5
5.
1.2.3
-9.5
```

---

# 13. ER-03 — Decimal

## 13.1 Definições

A parte inteira usa a mesma linguagem da ER-02:

\[
I=(0\mid ND^*)
\]

Definimos o ponto literal como:

\[
\boxed{P=\{\texttt{.}\}}
\]

Logo:

\[
\boxed{L_{DEC}= (0\mid ND^*)PDD^*}
\]

## 13.2 Alfabeto

\[
\Sigma_{DEC}=D\cup\{\texttt{.}\}
\]

## 13.3 Sintaxe Python

```python
r"(0|[1-9][0-9]*)\.[0-9]+"
```

Correspondência completa:

```python
re.fullmatch(
    r"(0|[1-9][0-9]*)\.[0-9]+",
    cadeia
)
```

## 13.4 Equivalência

| Formal | Python |
|---|---|
| `0` | `0` |
| `N` | `[1-9]` |
| `D` | `[0-9]` |
| `P` | `\.` |
| `D*` | `[0-9]*` |
| `DD*` | `[0-9]+` |

O símbolo `P` é uma decisão de notação do projeto para eliminar a ambiguidade do ponto na documentação.

## 13.5 AFNε definitivo

Estado inicial: `q0`  
Estado final: `q17`

\[
\boxed{18\text{ estados},\;22\text{ transições},\;16\varepsilon,\;6\text{ rotuladas}}
\]

| Origem | Símbolo | Destino |
|---|---|---|
| `q2` | `0` | `q3` |
| `q0` | `ε` | `q2` |
| `q3` | `ε` | `q1` |
| `q4` | `N` | `q5` |
| `q8` | `D` | `q9` |
| `q6` | `ε` | `q8` |
| `q6` | `ε` | `q7` |
| `q9` | `ε` | `q8` |
| `q9` | `ε` | `q7` |
| `q5` | `ε` | `q6` |
| `q0` | `ε` | `q4` |
| `q7` | `ε` | `q1` |
| `q10` | `P` | `q11` |
| `q1` | `ε` | `q10` |
| `q12` | `D` | `q13` |
| `q11` | `ε` | `q12` |
| `q16` | `D` | `q17` |
| `q14` | `ε` | `q16` |
| `q14` | `ε` | `q17` |
| `q17` | `ε` | `q16` |
| `q17` | `ε` | `q15` |
| `q13` | `ε` | `q14` |

`P` representa exclusivamente o ponto literal `.`. A parte fracionária possui um `D` obrigatório e pode receber dígitos adicionais por `D*`.

## 13.6 Validação cruzada AFNε × regex

A ER-03 foi validada comparando o AFNε com a regex de referência:

```python
r"(0|[1-9][0-9]*)\.[0-9]+"
```

Foram obtidos 24/24 resultados coincidentes nas baterias documentadas: 12 casos da bateria principal e 12 casos adicionais de fronteira. Não foi registrada divergência entre o AFNε e a regex de referência.

O estado final correto é `q17`. A referência histórica a `q15` como estado final foi corrigida nesta versão do guia.

# 14. Notação científica

A MiniLang terá uma quarta categoria numérica para criar uma linguagem regular mais rica e aproximar o lexer de uma linguagem de programação real.

Exemplos:

```text
1e3
1.5e3
9.5E-2
10.25e+4
```

O formato não aceitará:

```text
01e3
1e
1.5e
1.5.2e3
```

---

# 15. ER-04 — Número científico

## 15.1 Definições

\[
I=(0\mid ND^*)
\]

\[
P=\{\texttt{.}\}
\]

\[
X=\{\texttt{e},\texttt{E}\}
\]

\[
S=\{\texttt{+},\texttt{-}\}
\]

A linguagem definitiva é:

\[
\boxed{(0\mid ND^*)(PDD^*\mid\varepsilon)X(S\mid\varepsilon)DD^*}
\]

Forma expandida:

\[
\boxed{(0\mid ND^*)(PDD^*\mid\varepsilon)(\texttt{e}\mid\texttt{E})(\texttt{+}\mid\texttt{-}\mid\varepsilon)DD^*}
\]

## 15.2 Sintaxe Python

```python
r"(0|[1-9][0-9]*)(\.[0-9]+)?[eE][+-]?[0-9]+"
```

Correspondência completa:

```python
re.fullmatch(
    r"(0|[1-9][0-9]*)(\.[0-9]+)?[eE][+-]?[0-9]+",
    cadeia
)
```

## 15.3 Equivalência

| Formal | Python |
|---|---|
| `0` | `0` |
| `N` | `[1-9]` |
| `D` | `[0-9]` |
| `P` | `\.` |
| `PDD*` | `\.[0-9]+` |
| `PDD* | ε` | `(...)?` |
| `e | E` | `[eE]` |
| `+ | - | ε` | `[+-]?` |
| `DD*` | `[0-9]+` |

## 15.4 AFNε definitivo

A construção canônica de Thompson resulta em:

\[
\boxed{42\text{ estados},\;52\text{ transições},\;40\varepsilon,\;12\text{ rotuladas}}
\]

Estado inicial: `q0`  
Estado final: `q39`

### Tabela definitiva

| Origem | Símbolo | Destino |
|---|---|---|
| `q2` | `0` | `q3` |
| `q0` | `ε` | `q2` |
| `q3` | `ε` | `q1` |
| `q4` | `N` | `q5` |
| `q8` | `D` | `q9` |
| `q6` | `ε` | `q8` |
| `q6` | `ε` | `q7` |
| `q9` | `ε` | `q8` |
| `q9` | `ε` | `q7` |
| `q5` | `ε` | `q6` |
| `q0` | `ε` | `q4` |
| `q7` | `ε` | `q1` |
| `q12` | `P` | `q13` |
| `q14` | `D` | `q15` |
| `q13` | `ε` | `q14` |
| `q18` | `D` | `q19` |
| `q16` | `ε` | `q18` |
| `q16` | `ε` | `q17` |
| `q19` | `ε` | `q18` |
| `q19` | `ε` | `q17` |
| `q15` | `ε` | `q16` |
| `q10` | `ε` | `q12` |
| `q17` | `ε` | `q11` |
| `q20` | `ε` | `q21` |
| `q10` | `ε` | `q20` |
| `q21` | `ε` | `q11` |
| `q1` | `ε` | `q10` |
| `q24` | `e` | `q25` |
| `q22` | `ε` | `q24` |
| `q25` | `ε` | `q23` |
| `q26` | `E` | `q27` |
| `q22` | `ε` | `q26` |
| `q27` | `ε` | `q23` |
| `q11` | `ε` | `q22` |
| `q30` | `+` | `q31` |
| `q28` | `ε` | `q30` |
| `q31` | `ε` | `q29` |
| `q32` | `-` | `q33` |
| `q28` | `ε` | `q32` |
| `q33` | `ε` | `q29` |
| `q34` | `ε` | `q35` |
| `q28` | `ε` | `q34` |
| `q35` | `ε` | `q29` |
| `q23` | `ε` | `q28` |
| `q36` | `D` | `q37` |
| `q29` | `ε` | `q36` |
| `q40` | `D` | `q41` |
| `q38` | `ε` | `q40` |
| `q38` | `ε` | `q39` |
| `q41` | `ε` | `q40` |
| `q41` | `ε` | `q39` |
| `q37` | `ε` | `q38` |

A contagem definitiva é **42 estados, 52 transições, 40 ε e 12 transições rotuladas**. A contagem 38/47/36/11 está obsoleta e foi descartada após a rederivação canônica. A contagem válida para esta especificação é **42/52/40/12**.

## 15.5 Validação cruzada AFNε × regex

A ER-04 foi validada comparando o AFNε completo com a regex de referência:

```python
r"(0|[1-9][0-9]*)(\.[0-9]+)?[eE][+-]?[0-9]+"
```

### Bateria oficial

Foram testadas 12 cadeias: 5 aceitas e 7 rejeitadas. O AFNε e a regex produziram exatamente o mesmo resultado em **12/12** casos.

### Casos adicionais de fronteira

Foram testadas 7 cadeias adicionais, com **7/7** resultados coincidentes.

### Busca exaustiva reduzida

Também foi realizada uma comparação exaustiva para todas as cadeias de comprimento 0 até 5 sobre o alfabeto reduzido `{0,1,2,.,e,E,+,-}`. Não foi encontrada nenhuma divergência.

Resultado consolidado:

\[
\boxed{\text{0 divergências}}
\]

A equivalência observada nos testes é:

\[
\boxed{L(AFN_{\varepsilon,04})=L(REGEX_{04})}
\]

Com isso, a ER-04 está **validada e congelada**, permanecendo a implementação automatizada do lexer como etapa posterior.

## 15.6 Testes obrigatórios

### Aceitas

| Cadeia | Motivo |
|---|---|
| `1e3` | inteiro + `e` + expoente |
| `10e2` | inteiro + `e` + expoente |
| `0e5` | zero + `e` + expoente |
| `1.5e3` | decimal + `e` + expoente |
| `9.5E-2` | decimal + `E-` + expoente |
| `10.25e+4` | decimal + `e+` + expoente |

### Rejeitadas

| Cadeia | Motivo |
|---|---|
| `ε` | estrutura ausente |
| `1e` | falta o expoente |
| `1e+` | falta o dígito do expoente |
| `.5e2` | falta a parte inteira |
| `01e3` | zero à esquerda |
| `1.5.2e3` | dois pontos decimais |


# 16. Strings

## 16.1 Regra

Strings serão delimitadas por aspas duplas:

```text
"texto"
```

A string pode ser vazia:

```text
""
```

O conteúdo permitido será limitado a um conjunto ASCII definido.

Não serão permitidos:

```text
"
\
quebra de linha
tabulação
```

dentro do conteúdo.

Não haverá mecanismo de escape na primeira versão.

Isso foi decidido para manter uma correspondência clara com a construção de AFNε.

## 16.2 Exemplos válidos

```text
""
"Andrey"
"Hello World"
"Nota 9.5"
"idade > 18"
"arquivo.txt"
```

## 16.3 Exemplos inválidos

```text
"Andrey
Andrey"
"texto
quebrado"
"texto\"interno"
```

---

# 17. ER-05 — Literal de string

## 17.1 Conjunto de conteúdo

Definimos `C` como o conjunto ASCII permitido dentro da string:

\[
C=L\cup D\cup\{\text{espaço},\_,\texttt{.},\texttt{,},\texttt{!},\texttt{?},\texttt{:},\texttt{;},\texttt{+},\texttt{-},\texttt{*},\texttt{/},\texttt{=},\texttt{<},\texttt{>}\}
\]

A aspa dupla, a barra invertida, a tabulação e a quebra de linha não pertencem a `C`.

## 17.2 Alfabeto

\[
\Sigma_{STR}=C\cup\{\texttt{"}\}
\]

## 17.3 Linguagem

\[
\boxed{L_{STR}=\{\texttt{"}x\texttt{"}\mid x\in C^*\}}
\]

## 17.4 ER formal

\[
\boxed{\texttt{"}C^*\texttt{"}}
\]

A string vazia é aceita porque `C*` contém `ε`.

## 17.5 Sintaxe Python

```python
r'"[A-Za-z0-9 _.,!?;:+*/=<>-]*"'
```

Correspondência completa:

```python
re.fullmatch(
    r'"[A-Za-z0-9 _.,!?;:+*/=<>-]*"',
    cadeia
)
```

## 17.6 AFNε definitivo

Estado inicial: `q0`  
Estado final: `q7`

\[
\boxed{8\text{ estados},\;9\text{ transições},\;6\varepsilon,\;3\text{ rotuladas}}
\]

| Origem | Símbolo | Destino |
|---|---|---|
| `q0` | `"` | `q1` |
| `q4` | `C` | `q5` |
| `q2` | `ε` | `q4` |
| `q2` | `ε` | `q3` |
| `q5` | `ε` | `q4` |
| `q5` | `ε` | `q3` |
| `q1` | `ε` | `q2` |
| `q6` | `"` | `q7` |
| `q3` | `ε` | `q6` |

## 17.7 Testes obrigatórios

### Aceitas

```text
""
"Andrey"
"abc 123"
"a_b.c"
"hello!"
"12:30"
```

### Rejeitadas

```text
ε
"abc
abc"
"a"b"
"a\b"
"linha
```

O caso `""` é o limite positivo mais importante da ER-05.


# 18. Horário

Para ampliar a variedade das ERs sem criar uma linguagem desnecessariamente grande, a MiniLang terá um literal de horário.

Formato:

```text
HH:MM
```

onde:

```text
HH = 00 até 23
MM = 00 até 59
```

### Exemplos aceitos

```text
00:00
09:05
12:30
14:59
23:00
23:59
```

### Exemplos rejeitados

```text
24:00
12:60
2:30
14:5
99:99
14:30:00
```

---

# 19. ER-06 — Literal de horário

## 19.1 Alfabeto

\[
\Sigma_{TIME}=D\cup\{\texttt{:}\}
\]

Definimos:

\[
Q=\{\texttt{:}\}
\]

## 19.2 Linguagem

A hora pertence a `00–19` ou `20–23`, e os minutos pertencem a `00–59`.

## 19.3 ER formal

\[
\boxed{((0\mid1)D\mid2(0\mid1\mid2\mid3))Q(0\mid1\mid2\mid3\mid4\mid5)D}
\]

## 19.4 Sintaxe Python

```python
r"([01][0-9]|2[0-3]):[0-5][0-9]"
```

Correspondência completa:

```python
re.fullmatch(
    r"([01][0-9]|2[0-3]):[0-5][0-9]",
    cadeia
)
```

## 19.5 Equivalência

| Formal | Python |
|---|---|
| `(0|1)` | `[01]` |
| `D` | `[0-9]` |
| `2(0|1|2|3)` | `2[0-3]` |
| `Q` | `:` |
| `(0|1|2|3|4|5)` | `[0-5]` |

## 19.6 AFNε definitivo

Estado inicial: `q0`  
Estado final: `q15`

\[
\boxed{16\text{ estados},\;16\text{ transições},\;9\varepsilon,\;7\text{ rotuladas}}
\]

| Origem | Símbolo | Destino |
|---|---|---|
| `q2` | `01` | `q3` |
| `q4` | `D` | `q5` |
| `q3` | `ε` | `q4` |
| `q0` | `ε` | `q2` |
| `q5` | `ε` | `q1` |
| `q6` | `2` | `q7` |
| `q8` | `0123` | `q9` |
| `q7` | `ε` | `q8` |
| `q0` | `ε` | `q6` |
| `q9` | `ε` | `q1` |
| `q10` | `:` | `q11` |
| `q1` | `ε` | `q10` |
| `q12` | `012345` | `q13` |
| `q14` | `D` | `q15` |
| `q13` | `ε` | `q14` |
| `q11` | `ε` | `q12` |

`[01]`, `[0-3]`, `[0-5]` e `D` são rótulos agrupados para conjuntos finitos. A expansão símbolo a símbolo representa a mesma transição da construção.

## 19.7 Testes obrigatórios

### Aceitas

```text
00:00
09:05
12:30
14:59
23:00
23:59
```

### Rejeitadas

```text
ε
24:00
12:60
2:30
14:5
99:99
```

O par `23:59` / `24:00` é o principal caso-limite da ER-06.


# 20. Comentários

A MiniLang terá comentários de uma linha:

```text
// comentario
```

O comentário termina na quebra de linha.

Exemplo:

```text
int idade = 20; // idade do aluno
```

O comentário será ignorado na lista final de tokens.

## 20.1 Regra

O comentário começa com:

```text
//
```

e pode possuir zero ou mais caracteres válidos até a quebra de linha.

### Exemplos

```text
//
 // comentario
// idade do aluno
// nota = 9.5
```

## 20.2 Situação

A regra de comentários é **auxiliar do lexer** e não será utilizada como uma das seis ERs principais avaliadas.

Ela poderá ser documentada como uma ER auxiliar no relatório.

---

# 21. Operadores

Os operadores são:

## 21.1 Aritméticos

```text
+
-
*
/
```

## 21.2 Relacionais

```text
==
!=
<
>
<=
>=
```

## 21.3 Atribuição

```text
=
```

## 21.4 Estratégia

Os operadores serão reconhecidos por comparação direta com uma tabela, e não como uma das ERs principais do trabalho.

Isso evita criar uma ER trivial apenas para demonstrar:

```text
+|-|*|/|...
```

Ainda assim, os operadores fazem parte da MiniLang e serão testados pelo lexer.

---

# 22. Delimitadores

Os delimitadores são:

```text
(
)
{
}
;
,
```

Tabela:

| Símbolo | Token |
|---|---|
| `(` | LPAREN |
| `)` | RPAREN |
| `{` | LBRACE |
| `}` | RBRACE |
| `;` | SEMICOLON |
| `,` | COMMA |

Não haverá `[` e `]` na primeira versão.

---

# 23. Tokens oficiais

Os tokens principais serão:

```text
PROGRAM

TYPE_INT
TYPE_FLOAT
TYPE_STRING
TYPE_BOOL
TYPE_TIME

IF
ELSE
WHILE
PRINT

BOOLEAN

IDENTIFIER

INTEGER
DECIMAL
SCIENTIFIC
STRING
TIME

PLUS
MINUS
MULTIPLY
DIVIDE

ASSIGN
EQUAL
NOT_EQUAL
LESS
GREATER
LESS_EQUAL
GREATER_EQUAL

LPAREN
RPAREN
LBRACE
RBRACE
SEMICOLON
COMMA
```

Tokens internos:

```text
WHITESPACE
COMMENT
```

serão descartados na saída final.

---

# 24. Seis ERs principais avaliadas

A partir desta revisão, as Expressões Regulares principais serão:

| ER | Padrão | Complexidade esperada | Status |
|---|---|---:|---|
| ER-01 | Identificador estruturado | Alta | auditada e congelada |
| ER-02 | Inteiro sem zero à esquerda | Média | auditada e congelada |
| ER-03 | Decimal sem zero à esquerda | Média | auditada e congelada |
| ER-04 | Número científico | Alta | validada e congelada |
| ER-05 | Literal de string | Média | auditada e congelada |
| ER-06 | Literal de horário | Alta | auditada e congelada |

Há, portanto, seis ERs principais, acima do mínimo de cinco exigido.

As regras de:

```text
palavras reservadas
operadores
delimitadores
comentários
whitespace
```

fazem parte do lexer, mas não precisam ser usadas como ERs avaliadas principais.

---

# 25. Ordem oficial de tokenização

Esta ordem fica congelada para a implementação:

```text
1. whitespace
2. comentário
3. string
4. operador composto
5. número científico
6. número decimal
7. TIME
8. número inteiro
9. identificador / palavra reservada
10. operador simples
11. delimitador
12. erro léxico
```

O princípio é combinar prioridade com **maior lexema**, sem permitir que uma regra mais simples esconda um candidato inválido iniciado na mesma posição.


# 26. Justificativa da prioridade

## 26.1 Comentário antes de divisão

```text
//
```

deve ser reconhecido antes de:

```text
/
```

Caso contrário:

```text
// comentario
```

poderia virar:

```text
DIVIDE
DIVIDE
```

---

## 26.2 Operadores compostos antes de simples

Devemos verificar:

```text
==
!=
<=
>=
```

antes de:

```text
=
!
<
>
```

Assim:

```text
<=
```

vira:

```text
LESS_EQUAL
```

e não:

```text
LESS
ASSIGN
```

---

## 26.3 Científico antes de decimal

```text
1.5e3
```

deve virar:

```text
SCIENTIFIC
```

e não:

```text
DECIMAL
IDENTIFIER
```

---

## 26.4 Decimal antes de inteiro

```text
9.5
```

deve virar:

```text
DECIMAL
```

e não:

```text
INTEGER
```

seguido de caracteres restantes.

---

## 26.5 Identificador antes da consulta de palavra reservada

O lexer deve capturar o lexema completo.

Exemplo:

```text
integer
```

não deve ser fragmentado como:

```text
int
eger
```

O procedimento será:

```text
capturar o lexema completo
        ↓
verificar se ele está na tabela de reservadas
        ↓
se sim → palavra reservada
se não → IDENTIFIER
```

Assim:

```text
int
```

é:

```text
TYPE_INT
```

e:

```text
integer
```

é:

```text
IDENTIFIER
```

---

# 27. Regra de maior lexema e proteção contra tokenização parcial

O lexer não poderá aceitar somente um prefixo válido se o trecho seguinte mostrar que o candidato iniciado na mesma posição é um lexema numérico inválido.

## 27.1 Princípio para candidatos numéricos

Quando a posição atual começa com dígito, a implementação analisará uma candidata numérica formada por uma das estruturas:

```text
D+
D+ . D+
D+ e/E [+-]? D+
D+ . D+ e/E [+-]? D+
```

Também serão reconhecidos candidatos incompletos como `1e` e `1e+`, para que sejam reportados como erro léxico em vez de serem divididos em tokens menores.

O `+` e o `-` continuam sendo operadores quando aparecem fora de um expoente. Portanto:

```text
20+3  → INTEGER(20) PLUS INTEGER(3)
20-3  → INTEGER(20) MINUS INTEGER(3)
1e+3  → SCIENTIFIC(1e+3)
```

## 27.2 Validação do candidato

A prioridade interna é:

```text
posição começa com dígito
        ↓
formar candidato numérico
        ↓
SCIENTIFIC?
        ↓ não
DECIMAL?
        ↓ não
INTEGER?
        ↓ não
ERRO LÉXICO
```

Se `e` ou `E` aparecer depois da mantissa, ele passa a integrar o candidato científico. Nesse contexto, `+` ou `-` imediatamente depois de `e`/`E` pertence ao expoente.

## 27.3 Contaminação imediata

Depois de um número válido, letras e um novo ponto decimal não devem ser tratados como um novo token silenciosamente:

```text
10a    → erro
1e3a   → erro
1.2.3  → erro
01     → erro
01.5   → erro
```

Já operadores aritméticos fora do expoente permanecem separados:

```text
10+2   → INTEGER PLUS INTEGER
9.5-1  → DECIMAL MINUS INTEGER
```

## 27.4 Identificadores

Depois de reconhecer um lexema completo com formato de identificador, o lexer consulta a tabela de palavras reservadas. Não haverá fragmentação de `integer` em `int` + `eger`.

# 28. Erros léxicos

O MiniLexer deverá informar:

- linha;
- coluna;
- lexema ou trecho problemático;
- motivo.

Exemplo:

```text
ERRO LÉXICO

Linha: 3
Coluna: 9
Lexema: 01.50

Motivo:
Número decimal com zero à esquerda.
```

Outro:

```text
ERRO LÉXICO

Linha: 4
Coluna: 12
Lexema: 9.5.3

Motivo:
Formato numérico inválido.
```

Outro:

```text
ERRO LÉXICO

Linha: 5
Coluna: 14

Motivo:
String não encerrada.
```

Outro:

```text
ERRO LÉXICO

Linha: 6
Coluna: 20
Lexema: @

Motivo:
Símbolo não reconhecido pela MiniLang.
```

---

# 29. Entrada vazia

Uma entrada vazia deverá ser tratada explicitamente.

Caso:

```text
""
```

ou arquivo sem conteúdo.

Saída planejada:

```text
Nenhum código foi fornecido.

A análise léxica não foi realizada.
```

Isso atende à necessidade de tratar entradas vazias.

---

# 30. Distinção entre erro lexical e erro sintático

## Erro léxico

Acontece quando o analisador não consegue formar um lexema pertencente às categorias definidas.

Exemplo:

```text
@
```

## Erro sintático

Acontece quando os tokens são válidos, mas sua sequência não respeita a estrutura da linguagem.

Exemplo:

```text
int idade 20;
```

Todos esses trechos podem ser tokens válidos:

```text
TYPE_INT
IDENTIFIER
INTEGER
SEMICOLON
```

mas a organização pode ser sintaticamente incorreta.

**O MiniLexer não será responsável pela análise sintática.**

---

# 31. Estrutura conceitual de um programa

A linguagem permitirá exemplos deste tipo:

```text
program cadastro {

    int idade = 20;
    float nota = 9.5;
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
}
```

Esse código é um **exemplo de entrada léxica**.

O MiniLexer não promete verificar toda a sintaxe ou executar o programa.

---

# 32. Exemplo de tokenização

Entrada:

```text
int idade = 20;
```

Saída conceitual:

```text
TYPE_INT      "int"
IDENTIFIER    "idade"
ASSIGN        "="
INTEGER       "20"
SEMICOLON     ";"
```

Entrada:

```text
float nota = 9.5;
```

Saída:

```text
TYPE_FLOAT    "float"
IDENTIFIER    "nota"
ASSIGN        "="
DECIMAL       "9.5"
SEMICOLON     ";"
```

Entrada:

```text
time entrada = 14:30;
```

Saída:

```text
TYPE_TIME     "time"
IDENTIFIER    "entrada"
ASSIGN        "="
TIME          "14:30"
SEMICOLON     ";"
```

Entrada:

```text
float fator = 1.5e3;
```

Saída:

```text
TYPE_FLOAT    "float"
IDENTIFIER    "fator"
ASSIGN        "="
SCIENTIFIC    "1.5e3"
SEMICOLON     ";"
```

---

# 33. Exemplos que devem provocar erro

## 33.1 Identificador

```text
int 2idade = 20;
```

Erro no lexema:

```text
2idade
```

---

## 33.2 Inteiro

```text
int codigo = 007;
```

Na especificação atual:

```text
007
```

é inválido como `INTEGER`.

---

## 33.3 Decimal

```text
float nota = 09.5;
```

Inválido devido ao zero à esquerda.

---

## 33.4 Científico

```text
float fator = 1.5e;
```

Inválido porque falta o expoente numérico.

---

## 33.5 String

```text
string nome = "Andrey;
```

Inválido porque a string não foi fechada.

---

## 33.6 Horário

```text
time entrada = 25:90;
```

Inválido porque:

```text
25 > 23
90 > 59
```

---

## 33.7 Símbolo

```text
int idade = 20 @ 5;
```

`@` não pertence ao vocabulário atual.

---

# 33.1 Fechamento das ERs 03 e 04

- **ER-03:** 18 estados / 22 transições / 16 ε / 6 rotuladas; estado final `q17`; validação cruzada **24/24**, sem divergências.
- **ER-04:** 42 estados / 52 transições / 40 ε / 12 rotuladas; estado final `q39`; validação cruzada **12/12** na bateria oficial, **7/7** nos casos adicionais e **0 divergências** na busca exaustiva até comprimento 5 no alfabeto reduzido.

# 34. AFNε — política definitiva

## 34.1 Método

Todos os seis autômatos usam a mesma construção de Thompson, com concatenação por transição ε e classes finitas apresentadas como rótulos agrupados.

## 34.2 Tabela de referência congelada

| ER | Inicial | Final | Estados | Transições | ε | Rotuladas |
|---|---|---|---:|---:|---:|---:|
| ER-01 | `q0` | `q27` | 28 | 35 | 27 | 8 |
| ER-02 | `q0` | `q1` | 10 | 12 | 9 | 3 |
| ER-03 | `q0` | `q17` | 18 | 22 | 16 | 6 |
| ER-04 | `q0` | `q39` | 42 | 52 | 40 | 12 |
| ER-05 | `q0` | `q7` | 8 | 9 | 6 | 3 |
| ER-06 | `q0` | `q15` | 16 | 16 | 9 | 7 |

## 34.3 Regra de apresentação

A numeração dos estados, tabela de transições, diagramas e simulações deverá permanecer idêntica em todos os materiais.

Se uma classe agrupada for expandida para símbolos individuais, isso será explicitado como uma expansão da mesma transição, e não como uma nova construção.

Na versão atual, cada ER possui dois artefatos de diagrama no repositório:

```text
docs/diagramas/ER-XX/ER-XX.jff
docs/diagramas/ER-XX/ER-XX.md
```

O `.jff` é a representação para JFLAP e o `.md` contém o diagrama Mermaid. Ambos são derivados da mesma tabela canônica de transições. No `.jff`, cada classe é expandida em transições de um caractere (por exemplo, `D` vira dez transições, de `0` a `9`), porque o JFLAP 7.1 não interpreta rótulos como `[0-9]`; as contagens Thompson se referem às transições agrupadas.

## 34.4 Simulação

Para uma cadeia `w`, o simulador começa pelo `ε-fecho` do estado inicial. A cada símbolo aplica `move` e calcula novamente o `ε-fecho`. A cadeia é aceita somente quando todos os símbolos foram consumidos e algum estado final pertence ao conjunto de estados ativos.


# 35. Testes por ER

Cada ER principal deverá possuir:

```text
6 cadeias aceitas
6 cadeias rejeitadas
1 ou mais casos-limite
```

Os conjuntos de testes das seis ERs estão registrados nesta especificação e também são exercitados pelos validators automatizados.

Formato recomendado:

| Cadeia | Esperado | Resultado | Justificativa |
|---|---|---|---|
| exemplo | aceita | aceita | pertence a L |
| exemplo | rejeita | rejeita | não pertence a L |

Também haverá testes integrados para o MiniLexer.

---

# 36. Discussão de limitações

Cada ER deverá possuir uma seção de limitações.

Exemplos de limitações que podemos explorar:

## Identificadores

Uma regex consegue verificar o formato do nome, mas não pode decidir se a variável foi previamente declarada.

## Números

A ER verifica formato lexical, não valor matemático.

## Strings

A regra atual não possui mecanismo de escape.

## Horários

A ER verifica `00–23` e `00–59`, mas não decide se um horário faz sentido em um contexto específico.

## Científicos

A ER verifica formato, mas não realiza cálculo numérico.

Essas limitações são importantes para a discussão dos resultados.

---

# 37. O que não usaremos nas ERs avaliadas

Não utilizaremos:

```text
retorreferências
recursão
condicionais avançadas
lookaround
outros recursos que não possuam correspondência clara
com a construção formal de AFNε
```

A implementação deverá permanecer no conjunto de recursos básicos compatíveis com o material da disciplina.

---

# 38. Organização prevista do projeto

```text
minilexer/
│
├── src/
│   ├── lexer.py
│   ├── tokens.py
│   ├── patterns.py
│   └── main.py
│
├── tests/
│   ├── test_er01_identifier.py
│   ├── test_er02_integer.py
│   ├── test_er03_decimal.py
│   ├── test_er04_scientific.py
│   ├── test_er05_string.py
│   ├── test_er06_time.py
│   └── test_lexer.py
│
├── docs/
│   ├── er/
│   └── afne/
│
├── examples/
│   ├── valido.min
│   └── invalido.min
│
├── README.md
└── requirements.txt
```

---

# 39. Arquitetura conceitual do MiniLexer

```text
                 CÓDIGO MINILANG
                        │
                        ▼
                ┌───────────────┐
                │    MiniLexer  │
                └───────────────┘
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
       padrões       tabela         símbolos
       por ERs       keywords       fixos
          │             │             │
          └─────────────┼─────────────┘
                        ▼
                      TOKENS
                        │
                        ▼
                 RELATÓRIO LÉXICO
```

---

# 39.5. Registro histórico — pré-mortem da ER-01

A análise abaixo documenta riscos identificados durante a fase de implementação. Ela é um registro histórico de prevenção e não representa o estado atual do projeto.

| Risco | Sinal antecipado | Prevenção |
|---|---|---|
| Contagem Thompson incorreta | tabela e derivação apresentam números diferentes | derivar cada ER de dentro para fora e conferir estados/transições |
| Diagrama diferente da tabela | estado final ou inicial muda entre materiais | manter a mesma numeração em tabela, diagrama, simulação e código |
| AFNε aceita/rejeita diferente da ER | regex Python e simulador divergem | executar os mesmos casos contra ambos |
| `_` aceito em posição inválida | casos como `abc_` passam | manter a estrutura formal `L(A|_AA*)*` sem simplificá-la indevidamente |
| ε-fecho mal implementado | cadeias simples falham ou `ε` não é aceita | testar separadamente `ε-fecho`, `move` e aceitação |
| documentação fica atrasada | guia mantém contagem antiga | atualizar o MD imediatamente após cada fechamento de ER |

### Estado da ER-01

A ER-01 está **estruturalmente fechada, implementada e validada**. Sua construção é mantida na tabela canônica, no AFNε do código, no `.jff` do JFLAP e no diagrama Mermaid.

# 40. Estratégia de implementação — estado atual

As seis Expressões Regulares principais foram formalmente definidas, os AFNε correspondentes foram implementados e validados, e o MiniLexer passou a integrar essas regras em uma aplicação léxica funcional.

A sequência efetivamente realizada foi:

```text
1. Consolidar a especificação da MiniLang
2. Construir o simulador genérico de AFNε
3. Cadastrar e validar ER-02
4. Cadastrar e validar ER-01, ER-03, ER-04, ER-05 e ER-06
5. Automatizar a validação AFNε × regex
6. Implementar tokens e padrões do lexer
7. Implementar o MiniLexer
8. Implementar longest match e prioridade de tokens
9. Implementar keywords, comentários, operadores e delimitadores
10. Implementar diagnóstico de erros com linha e coluna
11. Criar exemplos `.min`
12. Ampliar testes integrados
13. Gerar e validar os diagramas JFLAP/Mermaid
14. Consolidar documentação e repositório
```

---

# 41. Correções e decisões consolidadas

As principais decisões teóricas permanecem congeladas. Durante a implementação, a validação automática encontrou e corrigiu três inconsistências de transcrição nas tabelas dos AFNε:

```text
✓ ER-01: correção do ramo iniciado em `_`
✓ ER-03: correção da saída da parte fracionária mínima
✓ ER-06: q8 → q9 utiliza 0123 para representar 0|1|2|3
```

Essas correções não alteram as contagens formais congeladas; corrigem apenas a conectividade das tabelas efetivamente implementadas.

As contagens vigentes são:

| ER | Estados | Transições | ε | Rotuladas | Status |
|---|---:|---:|---:|---:|---|
| ER-01 | **28** | **35** | **27** | **8** | **CONGELADA** |
| ER-02 | **10** | **12** | **9** | **3** | **CONGELADA** |
| ER-03 | **18** | **22** | **16** | **6** | **CONGELADA** |
| ER-04 | **42** | **52** | **40** | **12** | **CONGELADA** |
| ER-05 | **8** | **9** | **6** | **3** | **CONGELADA** |
| ER-06 | **16** | **16** | **9** | **7** | **CONGELADA** |

---

# 42. Critério para aceitar uma alteração na linguagem

Antes de adicionar qualquer recurso à MiniLang, a decisão deve responder às seis perguntas definidas pelo projeto:

```text
1. Ele é necessário?
2. É coerente com um analisador léxico?
3. Cria uma ER relevante?
4. Permite uma construção de AFNε clara?
5. Permite testes aceitos/rejeitados?
6. Pode ser explicado durante a apresentação?
```

Alterações que adicionem complexidade sem justificativa não devem entrar na primeira versão.

---

# 43. Regra de ouro do projeto

A complexidade deve ser consequência da linguagem, e não um objetivo em si.

```text
ER relevante
+
AFNε explicável
+
código correto
+
testes completos
+
comportamento demonstrável
```

---

# 44. Estado atual do projeto

O projeto já ultrapassou a etapa de especificação e validação isolada das ERs. Neste ponto existem três camadas efetivamente construídas:

```text
ESPECIFICAÇÃO
      ↓
AFNε
      ↓
MINILEXER
```

A especificação define seis ERs principais; os seis AFNε estão implementados e validados; o lexer integra os padrões e os tokens oficiais.

### Matriz de progresso

| Componente | Estado |
|---|---|
| Especificação MiniLang | ✓ concluída |
| ER-01 formal | ✓ |
| ER-02 formal | ✓ |
| ER-03 formal | ✓ |
| ER-04 formal | ✓ |
| ER-05 formal | ✓ |
| ER-06 formal | ✓ |
| AFNε das seis ERs | ✓ |
| Validação AFNε × regex | ✓ |
| Tokens oficiais | ✓ |
| Padrões do lexer | ✓ |
| MiniLexer | ✓ funcional |
| Longest match numérico | ✓ |
| Keywords | ✓ |
| Comentários | ✓ |
| Operadores compostos/simples | ✓ |
| Delimitadores | ✓ |
| Diagnóstico de erro | ✓ |
| Exemplos `.min` | ✓ |
| Testes integrados ampliados | ✓ |
| Diagramas finais | ✓ |
| Relatório técnico final | → pendente |
| Apresentação final | → pendente |

---

# 44.1 Validação formal e de implementação

A validação dos seis AFNε foi realizada contra as regexes Python de referência. O conjunto consolidado verificou:

| ER | Cadeias verificadas | Divergências |
|---|---:|---:|
| ER-01 | 3.906 | 0 |
| ER-02 | 111.111 | 0 |
| ER-03 | 364 | 0 |
| ER-04 | 19.608 | 0 |
| ER-05 | 19.531 | 0 |
| ER-06 | 177.156 | 0 |
| **Total** | **331.676** | **0** |

Os testes unitários e integrados também são mantidos separadamente para distinguir a validação das ERs da validação do comportamento completo do lexer.

---

# 45. Implementação dos AFNε

O simulador `AFNe` fornece:

```text
epsilon_fecho(estados)
mover(estados, simbolo)
aceita(cadeia)
simular(cadeia)
```

A simulação segue o ciclo:

```text
ε-fecho inicial
→ MOVE(symbol)
→ ε-fecho
→ MOVE(symbol)
→ ε-fecho
→ ...
→ verificação de estado final
```

As classes finitas são mantidas como rótulos agrupados na especificação e expandidas para símbolos individuais quando representadas computacionalmente.

---

# 46. Implementação do MiniLexer

A implementação foi organizada em:

```text
src/
├── automata.py
├── patterns.py
├── tokens.py
├── lexer.py
└── main.py
```

### 46.1 `tokens.py`

Concentra os tipos oficiais de tokens e a estrutura usada para representar cada lexema reconhecido.

### 46.2 `patterns.py`

Concentra as regexes de referência das seis ERs, a tabela de palavras reservadas, operadores e delimitadores.

### 46.3 `lexer.py`

Responsável por:

```text
leitura da entrada
→ identificação do candidato
→ aplicação da prioridade
→ seleção do maior lexema
→ criação do token
→ atualização de linha/coluna
```

### 46.4 `main.py`

Permite executar o lexer sobre arquivos `.min` e visualizar a saída léxica e os erros.

---

# 47. Ordem oficial de tokenização aplicada

A ordem continua congelada:

```text
1. whitespace
2. comentário
3. string
4. operador composto
5. número científico
6. número decimal
7. TIME
8. número inteiro
9. identificador / palavra reservada
10. operador simples
11. delimitador
12. erro léxico
```

A regra evita que padrões mais gerais escondam padrões mais específicos.

---

# 48. Longest match e proteção contra fragmentação

A implementação trata candidatos numéricos como uma unidade. O objetivo é impedir que um lexema inválido seja silenciosamente dividido em vários tokens válidos menores.

Casos críticos cobertos pelos testes incluem:

```text
007
09.5
01e3
1e
1e+
1.5.2
10a
1e3a
24:00
14:30:00
```

Casos válidos usados para verificar a competição entre categorias incluem:

```text
123
123.45
123e2
123.45e2
20:00
20
```

Fora do expoente, `+` e `-` permanecem operadores independentes.

---

# 49. Palavras reservadas e identificadores

O lexer captura o lexema inteiro do identificador e só depois consulta a tabela de palavras reservadas.

Assim:

```text
int       → TYPE_INT
integer   → IDENTIFIER
int2      → IDENTIFIER
false     → BOOLEAN
falsehood → IDENTIFIER
```

Essa etapa evita classificação parcial de palavras que apenas começam com um lexema reservado.

---

# 50. Comentários, operadores e delimitadores

`//` é tratado antes de `/`, evitando confundir comentário com divisão.

Os operadores compostos são reconhecidos antes dos simples:

```text
==
!=
<=
>=
```

Os operadores simples e os seis delimitadores definidos pelo projeto são reconhecidos por tabela direta.

---

# 51. Strings

A implementação mantém a regra da ER-05:

```text
""
"Andrey"
"abc 123"
```

são válidas.

Strings não possuem escapes na primeira versão da linguagem, e conteúdo fora do conjunto `C` é rejeitado.

Uma string não encerrada gera erro léxico em vez de produzir uma sequência artificial de tokens.

---

# 52. Diagnóstico de erros

Os erros léxicos são representados com informação suficiente para localizar o problema:

```text
linha
coluna
lexema/trecho problemático
motivo
```

Exemplos de condições tratadas:

```text
zero à esquerda
número científico incompleto
decimal inválido
horário fora da faixa
string não encerrada
símbolo desconhecido
```

---

# 53. Testes integrados — Ciclo 4

A suíte integrada foi ampliada em relação ao ciclo anterior. Foram adicionados **73 testes de integração**, cobrindo as principais combinações entre tokens e os caminhos de erro do lexer.

### Cobertura adicionada

```text
✓ palavras reservadas × identificadores
✓ programas MiniLang completos
✓ tokenização sem espaços
✓ operadores simples e compostos
✓ comentário × divisão
✓ strings e string vazia
✓ INTEGER / DECIMAL / SCIENTIFIC / TIME
✓ zeros à esquerda
✓ fragmentação indevida de números
✓ identificadores inválidos
✓ símbolos desconhecidos
✓ linha e coluna de erro
✓ CRLF, tabulações e linhas vazias
✓ delimitadores e vírgulas
✓ execução da CLI
✓ exemplos valido.min e invalido.min
```

### Resultado consolidado

```text
47 testes da suíte anterior
+ 73 novos testes integrados
= 120 testes coletados

120 aprovados
0 falhas
```

A coleção de testes é separada entre testes do simulador, testes das regexes, testes unitários do lexer e testes de integração.

---

# 54. Exemplos executáveis

O projeto possui:

```text
examples/
├── valido.min
└── invalido.min
```

O exemplo válido exercita declarações, atribuição, número decimal, número científico, horário, string, operadores e estruturas da linguagem.

O exemplo inválido contém pelo menos um erro lexical intencional. A execução do lexer interrompe a emissão de tokens no primeiro erro, comportamento definido para esta etapa.

---

# 55. Limitações atuais

As limitações da primeira versão continuam sendo principalmente léxicas:

## Identificadores

A regex valida formato, não declaração ou existência da variável.

## Números

As regras validam formato lexical; não realizam cálculo ou interpretação matemática.

## Strings

Não há escapes na primeira versão.

## Horários

A ER valida a faixa `00–23` para horas e `00–59` para minutos, mas não interpreta contexto.

## Linguagem

O projeto continua sendo somente um analisador léxico. Não há compilação, execução, análise semântica, geração de código ou máquina virtual.

---

# 56. Próximas etapas

A base funcional do lexer e a documentação técnica principal estão construídas. O trabalho restante concentra-se no fechamento dos artefatos acadêmicos e do repositório final:

```text
1. consolidar a documentação final das seis ERs
2. organizar o repositório e remover artefatos temporários
3. registrar as contribuições dos integrantes
4. declarar o uso de IA no README e/ou relatório
5. finalizar o relatório técnico
6. finalizar a apresentação
7. executar o ensaio final com perguntas e alterações de entrada
```

Nenhuma alteração das ERs principais deve ser feita sem repetir a cadeia de consistência:

```text
ER formal
↓
AFNε
↓
regex no código
↓
testes
↓
MiniLexer
```

---

# 57. Regra de entrega

Antes da entrega, o repositório deve conter:

```text
código-fonte
README.md
requirements/dependências
arquivos de teste
dados/exemplos
diagramas dos AFNε
ERs documentadas
registro das contribuições
relatório técnico
apresentação
```

A versão final deve ser reproduzível a partir de uma instalação limpa e todos os testes devem ser executados antes do envio.

---

# 58. Estado de fechamento do ciclo atual

```text
ESPECIFICAÇÃO                  ✓
SEIS ERs                      ✓
SEIS AFNε                     ✓
VALIDAÇÃO AFNε × REGEX        ✓
VALIDAÇÃO ESTRUTURAL          ✓
JFLAP + MERMAID               ✓
TOKENS                        ✓
PATTERNS                      ✓
MINILEXER                     ✓
LONGEST MATCH                 ✓
KEYWORDS                      ✓
COMENTÁRIOS                   ✓
OPERADORES                    ✓
DELIMITADORES                 ✓
ERROS LÉXICOS                 ✓
EXEMPLOS                      ✓
TESTES INTEGRADOS             ✓
README                         ✓

CONTRIBUIÇÕES                 →
DECLARAÇÃO DE IA              →
RELATÓRIO                     →
APRESENTAÇÃO                  →
ENSAIO DE DEFESA               →
```

O projeto encontra-se na fase de **consolidação dos artefatos de entrega**, e não mais na fase de implementação estrutural inicial.

