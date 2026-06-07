// int v[5];                         // 5 ints (índices 0–4)
// int v[3] = {10, 20, 30};
// int m[2][3] = {{1,2,3},{4,5,6}};  // matriz 2×3
// v[0] = 42;

#include <stdio.h>

int main(void) {
    int v[5] = {10, 20, 30, 40, 50};

    /* soma dos elementos */
    int soma = 0;
    for (int i = 0; i < 5; i++)
        soma += v[i];
    printf("soma = %d\n", soma);

    /* matriz 2x3 */
    int m[2][3] = {{1, 2, 3}, {4, 5, 6}};
    printf("m[1][2] = %d\n", m[1][2]);  /* 6 */
    return 0;
}