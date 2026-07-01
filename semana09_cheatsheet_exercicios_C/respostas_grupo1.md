# Respostas - Grupo 1: Operadores Aritméticos

## Perguntas fechadas

Q1: c) 3

Q2: b) 2

Q3: c) pre=11, x=11

Q4: b) pos=11, x=12

Q5: c) -3 e -2

## Perguntas abertas

### A1

Para `a=23` e `b=4`:

| Expressão | Seu resultado | PythonTutor |
|------------|:-------------:|:-----------:|
| `a / b`    | 5             | 5           |
| `a % b`    | 3             | 3           |
| `a * b`    | 92            | 92          |
| `a - b*5`  | 3             | 3           |

### A2

Em números negativos, o resto pode ser negativo porque em C a divisão inteira trunca em direção a zero. Para testar paridade com qualquer inteiro, compare o resto com zero:

```c
#include <stdio.h>

int main(void) {
    int n = -4;
    if (n % 2 == 0)
        printf("%d é par\n", n);
    else
        printf("%d é ímpar\n", n);
    return 0;
}
```

Se a intenção for testar ímpar, a forma correta continua sendo `n % 2 != 0`.