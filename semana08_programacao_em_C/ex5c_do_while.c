#include <stdio.h>

int main(void) {
    int n = 1;
    do {
        printf("n = %d\n", n);
        n *= 2;
    } while (n < 32);
    return 0;
}