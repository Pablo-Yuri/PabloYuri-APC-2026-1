# Apresentacao do Trabalho Final - Recorte C

## Sistema de Exploracao dos Microdados PDAD 2024
### Saude e acesso a servicos

**Disciplina:** Algoritmos e Programacao de Computadores  
**Formato:** dupla  
**Tempo de apresentacao:** 10 minutos

---

## 1. Tema do projeto

Nosso trabalho final trata do **Recorte C: Saude e acesso a servicos**.

**Pergunta central:**
qual e a cobertura de plano de saude e o uso de servicos de saude no DF?

O objetivo do sistema e permitir que a pessoa explore os dados da PDAD 2024 de forma visual e interativa, com filtros por Regiao Administrativa e comparacoes entre grupos etarios e faixas de renda.

---

## 2. Dados utilizados

Usamos os microdados da PDAD 2024 como base de analise.

- **Moradores:** arquivo CSV com informacoes individuais
- **Domicilios:** arquivo Excel com informacoes dos domicilios
- **Dicionario de variaveis:** referencia para interpretar os codigos das colunas

As variaveis principais do recorte sao:

- blocos **G** da tabela de moradores, ligados a saude
- `localidade`
- `idade_calculada`
- `renda_ind`

Tambem filtramos os valores sentinela `99999` e `88888` antes de qualquer calculo.

---

## 3. O que o sistema mostra

O sistema foi pensado para responder perguntas como:

- qual RA tem maior cobertura de plano de saude
- como a cobertura varia por faixa etaria
- se existe relacao entre renda e acesso a servicos
- quais grupos usam mais ou menos os servicos de saude

Na interface, o usuario consegue selecionar filtros e ver:

- graficos atualizados em tempo real
- estatisticas resumidas
- listas com resultados filtrados
- exportacao dos dados para arquivo

---

## 4. Funcionalidades principais

O sistema atende aos requisitos pedidos no trabalho:

- janela principal com descricao do recorte
- filtros interativos por RA com selecao escondida por caixas de marcacao
- aba propria para comparar duas ou mais RAs no proprio painel
- graficos embutidos com matplotlib
- estatisticas descritivas na propria interface
- exportacao dos resultados para `.txt` ou `.csv`
- organizacao do codigo em funcoes e variaveis em portugues

Se houver tempo, tambem podemos mostrar como a comparacao de RAs muda quando trocamos o indicador entre cobertura de plano e uso de servicos.

---

## 5. Analises implementadas

As analises do Recorte C podem ser apresentadas em tres eixos:

### 5.1 Cobertura de plano de saude por RA

Mostramos a proporcao de moradores com plano de saude em cada Regiao Administrativa.

### 5.2 Relacao com renda

Comparamos a cobertura de plano de saude entre faixas de renda para verificar se existe diferenca entre grupos.

### 5.3 Comparacao por idade

Separamos os moradores por grupos etarios para observar se o acesso aos servicos varia entre jovens, adultos e idosos.

---

## 6. Estrutura do codigo

Organizamos o projeto para facilitar manutencao e demonstracao:

- `Projeto_Final/codigo7.py`: interface principal em tkinter
- funcoes de leitura e limpeza dos dados
- funcoes de analise e calculo das estatisticas
- funcoes de exportacao dos resultados

Essa separacao ajuda a deixar a parte de analise independente da interface grafica. O codigo foi organizado com nomes de funcoes e variaveis em portugues para facilitar a leitura durante a apresentacao.

---

## 7. Demonstração ao vivo

Roteiro sugerido para a apresentacao:

1. abrir o sistema
2. mostrar o titulo e a descricao do recorte
3. abrir a selecao escondida de RAs e marcar duas ou mais unidades
4. trocar o indicador entre plano de saude e atendimento
5. ir para a aba de comparacao e observar o grafico atualizado
6. alterar a faixa etaria ou renda e notar a mudanca nas estatisticas
7. exportar um resumo para arquivo

Esse fluxo mostra que o sistema funciona sem precisar editar o codigo.

---

## 8. Por que escolhemos o Recorte C

Escolhemos este recorte porque ele permite discutir um tema social relevante e trabalhar com variaveis que aparecem de forma natural nos microdados da PDAD.

O assunto tambem facilita a combinacao de:

- leitura de dados com pandas
- tratamento de valores ausentes
- analise por grupos
- visualizacao com grafico
- interface grafica com tkinter

---

## 9. Conclusao

O projeto transforma os dados da PDAD 2024 em um sistema exploratorio simples de usar.

A ideia principal e ajudar a visualizar como a cobertura de plano de saude e o uso de servicos se distribuem no DF, destacando possiveis diferencas por regiao, idade e renda.

---

## 10. Possiveis perguntas da banca

- por que o recorte C foi escolhido?
- quais variaveis foram usadas e por que?
- como os valores `99999` e `88888` foram tratados?
- qual parte do sistema foi feita com tkinter?
- como o grafico e atualizado quando o filtro muda?

---

## 11. Observacao final

Este arquivo serve como base para a apresentacao oral. Ele pode ser adaptado para slides ou usado como roteiro da fala da dupla.