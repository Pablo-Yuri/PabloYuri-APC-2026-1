#include <stdio.h>

int main(void) {
    int dia = 3;   /* 1=Seg ... 7=Dom */

    switch (dia) {
        case 1: case 2: case 3: case 4: case 5:
            printf("Dia util\n");
            break;
        case 6: case 7:
            printf("Fim de semana\n");
            break;
        default:
            printf("Invalido\n");
    }
    return 0;
}