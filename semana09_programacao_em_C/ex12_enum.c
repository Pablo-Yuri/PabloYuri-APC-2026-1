// typedef enum { DOM=0, SEG, TER, QUA, QUI, SEX, SAB } DiaSemana;
// DiaSemana hoje = TER;   /* vale 2 */

#include <stdio.h>

typedef enum { DOM=0, SEG, TER, QUA, QUI, SEX, SAB } DiaSemana;

const char *nome_dia(DiaSemana d) {
    switch (d) {
        case DOM: return "Domingo";
        case SEG: return "Segunda";
        case TER: return "Terca";
        case QUA: return "Quarta";
        case QUI: return "Quinta";
        case SEX: return "Sexta";
        case SAB: return "Sabado";
        default:  return "???";
    }
}

int main(void) {
    for (DiaSemana d = DOM; d <= SAB; d++)
        printf("%d = %s\n", d, nome_dia(d));
    return 0;
}