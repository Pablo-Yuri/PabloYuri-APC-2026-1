#include <stdio.h>

int main(void) {
    int v[4] = {10, 20, 30, 40};
    int *p = v;          /* p aponta para v[0] */

    printf("*p      = %d\n", *p);       /* 10 */
    printf("*(p+1)  = %d\n", *(p+1));  /* 20 */
    printf("*(p+2)  = %d\n", *(p+2));  /* 30 */

    p++;                 /* agora aponta para v[1] */
    printf("apos p++: *p = %d\n", *p); /* 20 */
    return 0;
}