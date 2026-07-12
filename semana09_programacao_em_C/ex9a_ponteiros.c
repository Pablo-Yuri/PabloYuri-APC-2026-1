// int  x = 10;
// int *p = &x;    // p guarda o endereço de x
// *p = 20;        // derreferência: altera x via p

// // Aritmética de ponteiros
// int v[] = {1, 2, 3};
// int *p = v;
// p++;            // aponta para v[1]


#include <stdio.h>

int main(void) {
    int x = 10;
    int *p = &x;

    printf("x    = %d\n",  x);
    printf("&x   = %p\n",  (void*)&x);
    printf("p    = %p\n",  (void*)p);
    printf("*p   = %d\n",  *p);

    *p = 99;
    printf("x apos *p=99: %d\n", x);
    return 0;
}