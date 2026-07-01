# Respostas - Grupo 2: Operadores Relacionais

## Perguntas fechadas

Q1: c) 1

Q2: b) 1

Q3: b) `8 == 8` -> 1

Q4: c) `r8=99`, `a=99`

Q5: b) `r1=1  r2=0  r3=1  r4=1`

## Perguntas abertas

### A1

Para `a=5`, `b=10`, `c=5`:

| Expressão      | Seu resultado | PythonTutor |
|----------------|:-------------:|:-----------:|
| `a <= b`       | 1             | 1           |
| `b >= b`       | 1             | 1           |
| `c != a`       | 0             | 0           |
| `a + 5 != b`   | 0             | 0           |

### A2

O bug é usar `=` em vez de `==` dentro do `if`. Em C, `nota = 5` atribui 5 a `nota` e a expressão inteira vale 5, que é verdadeiro. Por isso o programa sempre entra no `if`.

Correção:

```c
#include <stdio.h>

int main(void) {
    int nota = 7;
    if (nota == 5)
        printf("nota é 5\n");
    else
        printf("nota não é 5\n");
    return 0;
}
```

Com `nota=7`, a saída correta é `nota não é 5`. Com `nota=5`, a saída é `nota é 5`.