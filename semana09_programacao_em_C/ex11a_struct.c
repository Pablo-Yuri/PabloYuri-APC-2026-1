// struct Ponto { int x; int y; };
// struct Ponto p = {3, 4};
// p.x = 10;

// typedef struct { float re; float im; } Complexo;

// struct Ponto *pp = &p;
// pp->x = 5;   /* equivale a (*pp).x = 5 */

// union Data { int i; float f; char c; };

#include <stdio.h>

typedef struct {
    int x;
    int y;
} Ponto;

float distancia(Ponto *a, Ponto *b) {
    int dx = a->x - b->x;
    int dy = a->y - b->y;
    /* evitamos sqrt para simplificar */
    return (float)(dx*dx + dy*dy);
}

int main(void) {
    Ponto origem = {0, 0};
    Ponto p      = {3, 4};

    printf("p.x=%d  p.y=%d\n", p.x, p.y);

    Ponto *ptr = &p;
    ptr->x = 10;
    printf("apos ptr->x=10: p.x=%d\n", p.x);

    printf("dist^2(origem,p) = %.0f\n", distancia(&origem, &p));
    return 0;
}