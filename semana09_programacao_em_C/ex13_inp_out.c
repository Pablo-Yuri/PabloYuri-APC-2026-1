// printf("x = %d, f = %.2f\n", x, f);
// scanf("%d %f", &x, &f);   // &: passa endereço!

// // %d int   %ld long   %f float   %lf double
// // %c char  %s string  %p ponteiro  %x hex

#include <stdio.h>

int main(void) {
    int    i = 255;
    float  f = 3.14159f;
    char   c = 'Z';
    char   s[] = "Brasilia";

    printf("Decimal:     %d\n",   i);
    printf("Hexadecimal: %x\n",   i);   /* ff */
    printf("Float 2dec:  %.2f\n", f);
    printf("Char:        %c\n",   c);
    printf("String:      %s\n",   s);
    printf("Ponteiro:    %p\n",   (void*)s);
    return 0;
}