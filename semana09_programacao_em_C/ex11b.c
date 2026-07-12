#include <stdio.h>

union Dado {
    int   i;
    float f;
    char  c;
};

int main(void) {
    union Dado d;
    d.i = 65;
    printf("d.i = %d\n",   d.i);
    printf("d.c = '%c'\n", d.c);  /* mesmo bytes, interpretado como char */
    d.f = 3.14f;
    printf("d.f = %.2f\n", d.f);
    /* d.i agora tem valor indefinido (sobrescrito por f) */
    return 0;
}