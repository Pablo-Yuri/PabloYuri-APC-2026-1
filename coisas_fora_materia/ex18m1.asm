    .cdecls "msp430.h"
    .global main

    .text

main:
    mov.w   #(WDTPW|WDTHOLD), &WDTCTL
    mov     #vetor, R12      
    mov     #5, R13 
    
    call    #extremos
    jmp     $
    nop


extremos:
    push    R4
    push    R5
    clr     R4
    mov.w   @R12, R5
extremos_loop:
    cmp     #0, R13
    jz      fim
    cmp     @R12, R4    ; --> R4 - @R12, negativo se @R12 for maior que R4 
    JL      novo_maior

    cmp     @R12, R5     ; -> R5 - @R12, positivo ou zero se R5 maior
    JGE     novo_menor

    jmp extremos_loop

novo_maior:
    mov     @R12, R4
    add     #2, R12
    dec     R13
    jmp     extremos_loop

novo_menor:
    mov     @R12, R5
    add     #2, R12
    dec     R13
    jmp     extremos_loop

fim:
    mov     R4, R12
    mov     R5, R13
    pop     R5
    pop     R4
    ret

; --- Dados ---
     .data
vetor: .word 1, 0, 3, 7, 0  

; ---------------------------------------------------
