// #include <stdlib.h>

// int *p = malloc(n * sizeof(int));
// if (!p) { /* erro */ }

// free(p);
// p = NULL;

#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int n = 4;
    int *v = malloc(n * sizeof(int));  /* aloca no heap */

    for (int i = 0; i < n; i++)
        v[i] = (i + 1) * 10;          /* 10 20 30 40 */

    for (int i = 0; i < n; i++)
        printf("v[%d] = %d\n", i, v[i]);

    free(v);    /* devolve ao heap */
    v = NULL;   /* evita uso acidental */
    return 0;
}