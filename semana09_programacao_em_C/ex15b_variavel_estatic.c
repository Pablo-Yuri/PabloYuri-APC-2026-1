#include <stdio.h>

void contador(void) {
    static int n = 0;   /* inicializado UMA VEZ; persiste */
    n++;
    printf("chamada numero %d\n", n);
}

int main(void) {
    contador();  /* 1 */
    contador();  /* 2 */
    contador();  /* 3 */
    return 0;
}