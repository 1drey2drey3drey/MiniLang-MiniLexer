# Comandos para a apresentação — MiniLexer

Execute os comandos a partir da **raiz do projeto**.

Antes da apresentação, instale o pytest (necessário para `python -m pytest`):

```powershell
pip install -r requirements.txt
```

## Validar uma ER específica

```powershell
python .\tests\validate_er01.py
python .\tests\validate_er02.py
python .\tests\validate_er03.py
python .\tests\validate_er04.py
python .\tests\validate_er05.py
python .\tests\validate_er06.py
```

## Validar todas as ERs

```powershell
python .\tests\validate_all.py
```

## Validar a estrutura dos AFNε

```powershell
python .\tests\validate_afne_structure.py
```

## Rodar todos os testes do projeto

```powershell
python -m pytest
```

## Apresentação rápida — sequência sugerida

```powershell
python .\tests\validate_er01.py
python .\tests\validate_er02.py
python .\tests\validate_er03.py
python .\tests\validate_er04.py
python .\tests\validate_er05.py
python .\tests\validate_er06.py
```

Ou, para mostrar a validação consolidada:

```powershell
python .\tests\validate_all.py
```

## Resultado esperado

Cada script termina indicando a validação da ER e, quando aplicável, as divergências. O resultado esperado é:

```text
0 divergências
```

Para a demonstração dos AFNε:

```powershell
python .\tests\validate_afne_structure.py
```

Resultado esperado:

```text
6/6 AFNε Python + 6/6 JFLAP
```
