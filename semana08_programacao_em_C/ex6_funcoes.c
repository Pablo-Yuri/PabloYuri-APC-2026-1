#include <stdio.h>

int fatorial(int n) {
    if (n <= 1) return 1;
    return n * fatorial(n - 1);  /* chamada recursiva */
}

void dobra(int *x) { *x *= 2; }

int main(void) {
    int f = fatorial(5);
    printf("5! = %d\n", f);

    int v = 7;
    dobra(&v);
    printf("dobro de 7 = %d\n", v);
    return 0;
}