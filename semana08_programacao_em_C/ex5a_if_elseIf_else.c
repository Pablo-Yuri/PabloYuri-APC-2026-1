#include <stdio.h>

int main(void) {
    int nota = 72;

    if      (nota >= 90) printf("A\n");
    else if (nota >= 80) printf("B\n");
    else if (nota >= 70) printf("C\n");
    else                 printf("Reprovado\n");

    return 0;
}