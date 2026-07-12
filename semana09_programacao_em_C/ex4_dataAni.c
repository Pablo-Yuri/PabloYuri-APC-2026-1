#include <stdio.h>

int main(void) {
    int a = 17, b = 5;

    printf("%d / %d = %d\n", a, b, a / b);  /* divisao inteira */
    printf("%d %% %d = %d\n", a, b, a % b); /* resto */

    int x = 3;
    int pre  = ++x;   /* x vira 4, pre  = 4 */
    int pos = x++;   /* pos = 4, x  vira 5 */
    printf("pre=%d  pos=%d  x=%d\n", pre, pos, x);

    int max = (a > b) ? a : b;
    printf("max(%d,%d) = %d\n", a, b, max);
    return 0;
}