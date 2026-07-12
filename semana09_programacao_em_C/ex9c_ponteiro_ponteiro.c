#include <stdio.h>

int main(void) {
    int  x  = 42;
    int *p  = &x;
    int **pp = &p;

    printf("x   = %d\n",   x);
    printf("*p  = %d\n",  *p);
    printf("**pp= %d\n", **pp);

    **pp = 100;           /* altera x via dois níveis de indireção */
    printf("x apos **pp=100: %d\n", x);
    return 0;
}