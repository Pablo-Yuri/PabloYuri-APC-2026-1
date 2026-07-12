# 📚 Guia de Instruções: Little Man Computer (LMC)

Este guia resume o conjunto de instruções (Instruction Set) do simulador **LMC**, um modelo simplificado da arquitetura de Von Neumann.

---

## 🏗️ Instruções de Memória e Aritmética
Estas instruções interagem entre o **Accumulator** (espaço de trabalho da CPU) e a **RAM** (gavetas de memória).

| Mnemônico | OpCode | Nome | Descrição |
| :--- | :--- | :--- | :--- |
| **LDA** | 5xx | Load | Copia o valor do endereço **xx** para o Acumulador. |
| **STA** | 3xx | Store | Copia o valor do Acumulador para o endereço de memória **xx**. |
| **ADD** | 1xx | Add | Soma o valor do endereço **xx** ao valor atual do Acumulador. |
| **SUB** | 2xx | Subtract | Subtrai o valor do endereço **xx** do valor atual do Acumulador. |

---

## 📤 Instruções de Entrada e Saída
Responsáveis pela interface com o usuário.

| Mnemônico | OpCode | Nome | Descrição |
| :--- | :--- | :--- | :--- |
| **INP** | 901 | Input | Solicita um número ao usuário e o armazena no Acumulador. |
| **OUT** | 902 | Output | Exibe o valor que está no Acumulador no console de saída. |

---

## 🔄 Instruções de Desvio (Branches)
Alteram o fluxo do programa modificando o **Program Counter (PC)**.

| Mnemônico | OpCode | Nome | Condição para o "Pulo" |
| :--- | :--- | :--- | :--- |
| **BRA** | 6xx | Branch Always | Pula sempre para o endereço **xx**. |
| **BRZ** | 7xx | Branch if Zero | Pula para **xx** apenas se o Acumulador for **0**. |
| **BRP** | 8xx | Branch if Positive| Pula para **xx** se o Acumulador for **0 ou maior**. |

---

## 🛑 Controle e Definição de Dados

| Mnemônico | OpCode | Nome | Descrição |
| :--- | :--- | :--- | :--- |
| **HLT** | 000 | Halt | Finaliza a execução do programa. |
| **DAT** | - | Data | Reserva um endereço de memória para armazenar dados (variáveis). |

---

## 💡 Dicas de Ouro para Provas (UnB)

1. **O Acumulador é volátil:** Quase todas as operações (`LDA`, `ADD`, `SUB`, `INP`) sobrescrevem o valor anterior do Acumulador. Use `STA` para salvar dados importantes.
2. **Ciclo FDE:** Lembre-se que o processo segue a ordem: **Fetch** (Busca no PC), **Decode** (Decodifica no CIR) e **Execute** (Realiza a tarefa).
3. **Endereçamento:** Nos OpCodes (ex: 510), o primeiro dígito é a **operação** e os dois últimos são o **endereço**.

---
*Gerado para Pablo - Estudante de Engenharia UnB - Google Gemini*