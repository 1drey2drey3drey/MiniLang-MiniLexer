# Explicações de estudo — MiniLang / MiniLexer

Esta pasta contém uma explicação detalhada de cada uma das seis Expressões Regulares principais do projeto. O objetivo é servir como material de estudo para compreender a relação:

```text
ER formal
   ↓
linguagem reconhecida
   ↓
regex Python
   ↓
AFNε
   ↓
MiniLexer
   ↓
testes
```

## Ordem recomendada de estudo

1. [ER-01 — Identificador estruturado](ER-01.md)
2. [ER-02 — Inteiro sem zero à esquerda](ER-02.md)
3. [ER-03 — Número decimal](ER-03.md)
4. [ER-04 — Número científico](ER-04.md)
5. [ER-05 — Literal de string](ER-05.md)
6. [ER-06 — Literal de horário](ER-06.md)

## Como estudar cada arquivo

Em cada ER, siga esta sequência:

```text
1. entenda qual linguagem deve ser reconhecida;
2. memorize as definições auxiliares;
3. decomponha a ER formal em blocos;
4. compare cada bloco com a regex Python;
5. entenda por que cada operador existe;
6. acompanhe o AFNε pelos seus blocos;
7. faça mentalmente um caminho aceito;
8. faça mentalmente um caminho rejeitado;
9. observe o caso-limite;
10. conecte tudo ao comportamento do MiniLexer;
11. execute o validator correspondente.
```

## Comandos

Validator individual:

```bash
python tests/validate_er01.py
python tests/validate_er02.py
python tests/validate_er03.py
python tests/validate_er04.py
python tests/validate_er05.py
python tests/validate_er06.py
```

Validator estrutural dos seis AFNε:

```bash
python tests/validate_afne_structure.py
```

Validação geral:

```bash
python tests/validate_all.py
```
