# Respostas - Grupo 4: Operadores Bit a Bit

## Perguntas fechadas

Q1: b) `00001100` = 12

Q2: c) `00111111` = 63

Q3: c) `00110011` = 51

Q4: b) multiplica por 4, resultando em 240

Q5: d) limpar o bit 3 de `flags`

## Perguntas abertas

### A1

Para `a=0b00111100` e `b=0b00001111`:

| Expressão   | Binário (8 bits) | Decimal | PythonTutor |
|-------------|:----------------:|:-------:|:-----------:|
| `a & b`     | `00001100`       | 12      | 12          |
| `a | b`     | `00111111`       | 63      | 63          |
| `a ^ b`     | `00110011`       | 51      | 51          |
| `a >> 2`    | `00001111`       | 15      | 15          |
| `~a & 0xFF` | `11000011`       | 195     | 195         |

### A2

Valores esperados:

| Passo | Operação       | Binário esperado | Decimal |
|-------|----------------|:----------------:|:-------:|
| Inicial | `x = 13`     | `00001101`       | 13      |
| 1     | seta bit 1     | `00001111`       | 15      |
| 2     | limpa bit 0    | `00001110`       | 14      |
| 3     | toggle bit 4   | `00011110`       | 30      |

Exemplo de raciocínio:

```c
x |= (1 << 1);
x &= ~(1 << 0);
x ^= (1 << 4);
```