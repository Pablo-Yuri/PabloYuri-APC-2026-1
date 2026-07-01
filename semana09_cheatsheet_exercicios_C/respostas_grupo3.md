# Respostas - Grupo 3: Operadores Lógicos

## Perguntas fechadas

Q1: c) 1

Q2: c) 1

Q3: b) 1

Q4: a) Não

Q5: a) Não

## Perguntas abertas

### A1

A condição `(x > 0) && (x % 2 == 0)` é verdadeira somente para inteiros positivos e pares.

| `x` | Esperado | PythonTutor |
|-----|:--------:|:-----------:|
| -4  | falso    | falso       |
| 0   | falso    | falso       |
| 3   | falso    | falso       |
| 4   | verdadeiro | verdadeiro |
| 8   | verdadeiro | verdadeiro |

### A2

O curto-circuito evita avaliar a segunda parte quando a primeira já decide o resultado. Isso é útil para impedir acesso indevido a ponteiros nulos, chamadas caras ou efeitos colaterais desnecessários.

Correção do programa:

```c
#include <stdio.h>

int seguro(int *p) {
    printf("  [acessando *p]\n");
    return *p > 0;
}

int main(void) {
    int v = 42;
    int *p = &v;

    if (p != NULL && seguro(p))
        printf("valor positivo\n");
    else
        printf("ponteiro nulo ou valor <= 0\n");

    return 0;
}
```

Se `p = NULL`, `seguro(p)` não é chamada por causa do `&&`, então não há desreferenciação de ponteiro nulo.