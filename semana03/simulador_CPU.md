# Semana 03

O objetivo da semana 02 se consistia em, criar um programa que contasse de 0 a um valor dado pelo usuário, usando o Little Man Computer, tecnologia apresentada em aulas anteriores.


---

### Abaixo o código desenvolvido com alguns comentários sobre seu funcionamento
> Logo depois o código sem comentários.

```
        INP          // O usuário digita o limite (ex: 5)
        STA limite   // Salva esse valor na memória
        
        LDA zero     // Começa o contador em 0 (carrega o contador)
loop    STA atual    // Salva o progresso do contador
        OUT          // Exibe o número atual no Output
        
        // Verificação: Caso o limite seja 0 o programa para
        LDA limite   
        SUB atual    // Faz (Limite - Atual), o limite voltará a ser o INP no próximo loop
        BRZ fim      // Se o resultado for 0, pula para o fim
        
        // Incremento
        LDA atual    // carrega o valor atual
        ADD um       // Soma +1
        BRA loop     // Volta para o início do laço
        
fim HLT // Finaliza o programa

zero    DAT 0
um      DAT 1
limite  DAT          // Reservado para o valor do INP
atual   DAT          // Reservado para o contador

```
### Código sem comentários

```
	INP         
        STA limite   
        
        LDA zero     
loop    STA atual    
        OUT          
        
        
        LDA limite   
        SUB atual    
        BRZ fim      
        
        LDA atual    
        ADD um       
        BRA loop     
        
fim HLT    

zero    DAT 0
um      DAT 1
limite  DAT          
atual   DAT        
```