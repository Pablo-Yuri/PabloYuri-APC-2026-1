#include <stdio.h>

int main(void) {
    int a = 42;
    int b;          /* valor lixo — NÃO leia antes de atribuir */
    // printf("b = %d -> Valor do lixo\n", *b );
    b = a + 8;

    printf("a = %d\n", a);
    printf("b = %d -> Valor B definido\n", b);

    const int N = 100;
    /* N = 200; */  /* descomente para ver o erro de compilacao */
    printf("N = %d\n", N);
    return 0;
}