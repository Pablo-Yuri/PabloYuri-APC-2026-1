#include <stdio.h>

int main(void) {
    int x = 1;
    printf("x externo = %d\n", x);

    {
        int x = 2;   /* nova variavel, esconde a externa */
        printf("x interno = %d\n", x);
    }

    printf("x externo apos bloco = %d\n", x);  /* ainda 1 */
    return 0;
}