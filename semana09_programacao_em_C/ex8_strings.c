// char s[] = "hello";      // 6 bytes: h e l l o \0
// char *p  = "hello";      // ponteiro para literal (imutável)

// strlen(s)        // comprimento sem '\0'
// strcpy(dst, src) // cópia
// strcmp(a, b)     // 0 se iguais


#include <stdio.h>
#include <string.h>

int main(void) {
    char s[] = "Brasilia";
    int  len = strlen(s);

    printf("Comprimento: %d\n", len);

    /* percorre e imprime cada char e seu codigo ASCII */
    for (int i = 0; i < len; i++)
        printf("s[%d] = '%c'  (ASCII %d)\n", i, s[i], s[i]);

    /* comparacao */
    char t[] = "Brasilia";
    printf("strcmp: %d\n", strcmp(s, t));  /* 0 = iguais */
    return 0;
}