# Linux & Terminal — Guia de Referência Rápida
**Disciplina:** Algoritmos e Programação de Computadores — APC 2026/1
**Licenciatura em Computação — UnB**

---

## O que é o Linux e por que usar?

O Linux é um sistema operacional de código aberto amplamente utilizado na área de tecnologia. No terminal (CLI), você interage diretamente com o sistema através de comandos, o que permite maior controle, automação e eficiência no desenvolvimento de software.

A estrutura de arquivos do Linux é organizada em uma árvore única, começando pela raiz `/`. Diferente do Windows, não existem letras de unidade (como `C:`); tudo está pendurado no "root".



---

## 1. Navegação e Localização

| Comando | Descrição | Exemplo |
|---|---|---|
| `pwd` | Mostra o caminho da pasta atual | `pwd` |
| `ls` | Lista arquivos e pastas | `ls -lh` (formato legível) |
| `cd` | Entra em um diretório | `cd Documents/APC` |
| `cd ..` | Volta um nível na hierarquia | `cd ..` |
| `cd ~` | Vai direto para sua pasta pessoal | `cd ~` |

---

## 2. Manipulação de Arquivos e Pastas

```bash
# Criar uma nova pasta (diretório)
mkdir exercicios_semana09

# Criar um arquivo de texto vazio
touch programa.py

# Copiar arquivos ou pastas (origem -> destino)
cp programa.py backup_programa.py

# Mover ou renomear arquivos
mv programa.py main.py

# Remover arquivos (CUIDADO: ação permanente)
rm antigo.txt

# Remover uma pasta e tudo dentro dela
rm -rf pasta_de_testes/

```
---

## 3. Lendo e Editando Arquivos

Para programar em APC, você usará editores de texto. Alguns funcionam dentro do próprio terminal, o que é ideal para edições rápidas ou via SSH.

| Comando | Função |
|---|---|
| `cat` | Exibe todo o conteúdo do arquivo na tela de uma vez |
| `head` / `tail` | Mostra as primeiras ou últimas 10 linhas do arquivo |
| `grep` | Busca uma palavra ou padrão específico dentro de um arquivo |
| `nano` | Editor simples e intuitivo (recomendado para começar) |
| `vim` | Editor profissional (poderoso, mas com comandos próprios) |

**Exemplo com Nano:**
`nano programa.py` $\rightarrow$ Edite o código $\rightarrow$ `Ctrl+O` (Salvar) $\rightarrow$ `Enter` $\rightarrow$ `Ctrl+X` (Sair).

---

## 4. Permissões de Arquivo

O Linux é rigoroso com segurança. Cada arquivo tem permissões de **Leitura (r)**, **Escrita (w)** e **Execução (x)** para o Dono, Grupo e Outros usuários.



```bash
# Ver as permissões detalhadas de um arquivo
ls -l programa.py
# Saída ex: -rwxr-xr-x (Dono pode tudo, outros só ler e executar)

# Dar permissão de execução para um script ou programa
chmod +x script.sh

# Rodar um comando como "Super Usuário" (Administrador do sistema)
sudo apt update