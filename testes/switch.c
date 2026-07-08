#include <stdio.h>

int main(void) {
    int x;
    printf("Digite um numero inteiro: ");
    scanf("%d", &x);

    switch (x) {
        case 1:
            printf("x = 1\n");
            break;
        case 2:
            printf("x = 2\n");
            break;
        default:
            printf("x = %d\n", x);
    }
    return 0;
}