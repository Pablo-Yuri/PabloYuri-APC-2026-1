// #define PI  3.14159
// #define MAX(a,b) ((a)>(b)?(a):(b))  // macro com parâmetros

// #ifdef DEBUG
//     printf("debug: x=%d\n", x);
// #endif

#include <stdio.h>

#define PI        3.14159
#define QUADRADO(x) ((x)*(x))
#define MAX(a,b)  ((a)>(b)?(a):(b))

int main(void) {
    double r = 5.0;
    printf("Area do circulo r=5: %.2f\n", PI * QUADRADO(r));

    int a = 7, b = 3;
    printf("MAX(%d,%d) = %d\n", a, b, MAX(a,b));

    /* armadilha classica de macro sem parenteses */
    printf("QUADRADO(a+1) = %d\n", QUADRADO(a+1)); /* (a+1)*(a+1) = 64 */
    return 0;
}