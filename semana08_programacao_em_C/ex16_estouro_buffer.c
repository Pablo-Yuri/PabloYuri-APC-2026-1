#include <stdio.h>
#include <string.h>

int main(void) {
    char destino[8];

    /* SEGURO: limita a copia ao tamanho do buffer */
    strncpy(destino, "Brasilia-DF", sizeof(destino) - 1);
    destino[sizeof(destino) - 1] = '\0';   /* garante terminador */

    printf("destino = '%s'\n", destino);
    printf("strlen  = %zu\n",  strlen(destino));
    return 0;
}