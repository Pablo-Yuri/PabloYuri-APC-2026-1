#include <stdlib.h>  
#include <stdio.h>  

typedef struct Pilha {
    int topo;  
    int dados[5];            
} Pilha;

void init(Pilha *gean) {
    gean->topo = 0;  
    return 0;
}

int main() {
    printf("%d\n", sizeof(Pilha));
    Pilha* p = malloc(sizeof(Pilha));
    printf("%d\n", p);
    
    init(p);        
    p->topo=0xffffffff;
    printf("%d",p->topo);
    return 0;                     
}