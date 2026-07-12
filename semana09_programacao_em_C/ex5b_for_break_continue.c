#include <stdio.h>

int main(void) {
    for (int i = 0; i < 10; i++) {
        if (i % 2 == 0) continue; /* pula pares */
        if (i == 7)     break;    /* para no 7  */
        printf("%d\n", i);
    }
    return 0;
}