# Git & GitHub — Guia de Referência Rápida
**Disciplina:** Algoritmos e Programação de Computadores — APC 2026/1
**Licenciatura em Computação — UnB**

---

## O que é o Git e por que usar?

O Git é um sistema distribuído de **controle de versão**: ele registra o histórico completo de todas as alterações feitas nos seus arquivos. Imagine que cada `commit` é uma foto do seu projeto num momento específico — você pode voltar a qualquer foto quando quiser.

Para sincronizar repositórios entre máquinas, o Git implementa um protocolo de comunicação próprio em nível de aplicação — mas um repositório Git funciona integralmente offline, sem nenhuma conexão necessária para as operações sobre o histórico local.

O **GitHub** é um dos sites que hospedam repositórios Git na internet, permitindo compartilhar código, colaborar com colegas e construir um portfólio público.

> Sem Git: `trabalho_final_v2_definitivo_ESSE.py`
> Com Git: um único arquivo com histórico completo e organizado.

Os arquivos armazenados em repositórios Git devem ser orientados a texto (código-fonte, Markdown, CSV, JSON etc.). Evite inserir documentos em formatos binários proprietários como DOCX ou PPTX — o Git não consegue calcular diferenças significativas entre versões desses arquivos.

---

## O repositório local — como o Git armazena tudo

Quando você executa `git init` ou `git clone`, o Git cria uma pasta oculta chamada `.git/` na raiz do projeto. Essa pasta **é** o repositório — tudo que o Git precisa está lá dentro:

```
.git/
├── objects/       ← todos os objetos do projeto: blobs, trees, commits, tags
├── refs/          ← ponteiros para branches e tags (arquivos de texto com hashes)
├── HEAD           ← indica em qual branch você está agora
├── index          ← a staging area (área de preparação)
├── config         ← configurações locais do repositório
└── logs/          ← histórico de movimentação das referências
```

A pasta onde você edita seus arquivos (a **pasta de trabalho**) é conceitualmente separada do repositório. O Git enxerga três zonas distintas:

```
Pasta de trabalho  →  Staging area (.git/index)  →  Repositório (.git/objects)
   (você edita)          (git add)                       (git commit)
```

O repositório local é **completo e autossuficiente** — não é um cache ou espelho parcial do remoto. Quando você faz `git clone`, recebe uma cópia integral de todo o histórico: todos os commits, todas as branches, todos os objetos. Consequências práticas importantes:

- `git log`, `git diff`, `git checkout` e `git branch` funcionam **sem conexão com a internet**
- se o GitHub saísse do ar, qualquer clone existente contém tudo que é necessário para reconstituir o repositório integralmente em outro lugar
- o `push` e o `pull` são operações de **sincronização entre iguais**, não de upload/download para um servidor autoritativo

Isso é o que distingue o Git de sistemas centralizados como SVN ou CVS, onde o histórico fica no servidor e o cliente tem apenas uma cópia de trabalho da versão atual.

> **Nunca edite manualmente o conteúdo da pasta `.git/`** — você pode corromper o repositório. Todas as operações devem ser feitas pelos comandos `git`.

---

## Conceitos essenciais

| Termo | Significado |
|---|---|
| **repositório** | pasta ou diretório onde se encontram os arquivos do projeto monitorados quanto às alterações; o repositório em si é a pasta `.git/` dentro dela |
| **commit** | registro de uma situação dos arquivos do projeto em um determinado instante de tempo (uma "foto"); identificado por um hash SHA-1 único |
| **branch** | linha paralela de desenvolvimento, com alterações que podem seguir rumos diferentes |
| **main** | branch principal do desenvolvimento, ao qual podem futuramente ser integradas as alterações feitas nos demais branches (nome padrão atual) |
| **remote** | repositório remoto com o qual o repositório local pode se sincronizar via `push` e `pull` |
| **origin** | apelido padrão dado ao repositório remoto de onde o projeto foi clonado; por convenção de equipe costuma ser o repositório de referência no GitHub ou GitLab, mas do ponto de vista do Git não tem estatuto diferente de qualquer outro remoto |
| **staging area** | área de preparação dentro de `.git/index` — onde você seleciona quais alterações vão entrar no próximo commit |
| **push** | sincronizar commits locais enviando-os para o repositório remoto |
| **pull** | sincronizar trazendo commits do repositório remoto para o local |
| **clone** | criar uma cópia local completa de um repositório remoto, incluindo todo o histórico |
| **merge** | integrar as alterações de uma branch em outra |
| **pull request** | pedido formal de revisão e merge, submetido para análise pelos responsáveis pelo repositório de referência; funcionalidade do GitHub/GitLab, não do Git em si |

---

## 1. Configuração inicial (fazer uma vez só por máquina)

```bash
# Registrar seu nome — aparece em cada commit que você fizer
git config --global user.name "Seu Nome Completo"

# Registrar seu e-mail — deve ser o mesmo cadastrado no GitHub
git config --global user.email "seu@email.com"

# Definir "main" como nome padrão de branch (padrão atual do GitHub)
git config --global init.defaultBranch main

# Fazer o Git salvar suas credenciais para não pedir toda vez
git config --global credential.helper store

# Verificar se ficou correto
git config --list
```

---

## 2. Criando um repositório

### Opção A — Iniciar do zero no seu computador

```bash
# Entrar na pasta do projeto (ou criar uma nova)
mkdir APC-2026-1
cd APC-2026-1

# Inicializar o repositório Git nessa pasta
# Isso cria uma pasta oculta .git que monitora tudo
git init

# Criar um arquivo README para começar
echo "# Meu Portfólio — APC 2026/1" > README.md

# Adicionar o arquivo à staging area (preparar para o commit)
git add README.md

# Registrar o primeiro commit
git commit -m "feat: primeiro commit — README inicial"

# Renomear a branch para "main" se ainda estiver como "master"
git branch -M main

# Conectar ao repositório criado no GitHub
# Substitua "usuario" e "APC-2026-1" pelos seus dados reais
git remote add origin https://github.com/usuario/APC-2026-1.git

# Enviar para o GitHub pela primeira vez
# -u configura o rastreamento — nas próximas vezes basta "git push"
git push -u origin main
```

### Opção B — Clonar um repositório que já existe no GitHub

```bash
# Baixa o repositório inteiro para o seu computador
git clone https://github.com/usuario/APC-2026-1.git

# Entra na pasta criada
cd APC-2026-1
```

---

## 3. Fluxo básico do dia a dia

Este é o ciclo que você vai repetir toda semana:

```bash
# 1. Ver o estado atual — quais arquivos foram modificados?
git status

# 2. Ver exatamente o que mudou dentro dos arquivos
git diff

# 3. Adicionar arquivos específicos à staging area
git add semana03/calculadora.py

# Ou adicionar TUDO que mudou de uma vez (cuidado — revise antes)
git add .

# 4. Registrar o commit com uma mensagem descritiva
git commit -m "feat: calculadora com operações básicas e tratamento de erros"

# 5. Enviar para o GitHub
git push
```

> **Regra de ouro:** `git status` antes de qualquer outra coisa. Sempre.

---

## 4. Mensagens de commit — como escrever bem

Uma boa mensagem de commit explica **o que mudou e por quê**, não apenas "atualizei o arquivo".

### Prefixos recomendados (convenção semântica)

| Prefixo | Quando usar |
|---|---|
| `feat:` | adicionou uma funcionalidade nova |
| `fix:` | corrigiu um bug |
| `docs:` | alterou documentação ou README |
| `refactor:` | reorganizou o código sem mudar o comportamento |
| `test:` | adicionou ou corrigiu testes |
| `style:` | formatação, identação, comentários |

### Exemplos

```bash
# Ruim — não diz nada
git commit -m "alterações"
git commit -m "arrumei"
git commit -m "semana 3"

# Bom — específico e descritivo
git commit -m "feat: calculadora com while para repetição e validação de entrada"
git commit -m "fix: corrige divisão por zero na função calcular()"
git commit -m "docs: atualiza README com reflexão da semana 3"
git commit -m "refactor: separa lógica da calculadora em funções individuais"
```

---

## 5. Inspecionando o histórico

```bash
# Ver o histórico de commits (do mais recente ao mais antigo)
git log

# Versão resumida — uma linha por commit (muito mais legível)
git log --oneline

# Versão gráfica — mostra branches e merges visualmente
git log --oneline --graph --all

# Ver as alterações de um commit específico
# Substitua o hash pelo código do commit (os 7 primeiros caracteres bastam)
git show a3f9c12

# Ver quem alterou cada linha de um arquivo
git blame semana03/calculadora.py
```

---

## 6. Desfazendo coisas

```bash
# Desfazer alterações em um arquivo que ainda NÃO foi para o staging
# (volta ao estado do último commit)
git checkout -- nome_do_arquivo.py

# Retirar um arquivo do staging sem perder as alterações
# (você adicionou com "git add" mas mudou de ideia)
git restore --staged nome_do_arquivo.py

# Corrigir a mensagem do ÚLTIMO commit (antes de fazer push)
git commit --amend -m "feat: mensagem corrigida"

# Voltar ao estado de um commit anterior SEM apagar o histórico
# (cria um novo commit que desfaz as mudanças)
git revert a3f9c12

# ⚠️ CUIDADO — apaga commits permanentemente (não use se já fez push)
git reset --hard a3f9c12
```

---

## 7. Branches — trabalhar em paralelo

Branches permitem desenvolver uma funcionalidade nova sem quebrar o que já funciona no `main`.

```bash
# Ver todas as branches existentes
git branch

# Criar uma branch nova
git branch semana09-funcoes

# Mudar para essa branch
git checkout semana09-funcoes

# Criar E já mudar para ela (atalho dos dois comandos acima)
git checkout -b semana09-funcoes

# Trabalhar normalmente, fazer commits...
git add .
git commit -m "feat: lib_matematica com funções mdc, mmc e primalidade"

# Voltar para a branch main
git checkout main

# Unir (merge) a branch de trabalho na main
git merge semana09-funcoes

# Deletar a branch depois de unir (já não precisa mais dela)
git branch -d semana09-funcoes

# Enviar uma branch para o GitHub
git push origin semana09-funcoes
```

---

## 8. Sincronizando com o GitHub

```bash
# Enviar commits locais para o GitHub
git push

# Buscar novidades do GitHub sem aplicar ainda
git fetch

# Buscar E aplicar as novidades (fetch + merge em um comando)
git pull

# Se for a primeira vez enviando uma branch nova
git push -u origin nome-da-branch
```

> **Antes de começar a trabalhar**, sempre faça `git pull` para garantir que você está com a versão mais recente.

---

## 9. Trabalhando com colegas — Pull Request

Um Pull Request (PR) é a forma de propor que seu trabalho seja incorporado ao projeto. No contexto da disciplina, é usado para entregar os estudos dirigidos e para colaborar no projeto final.

**Fluxo completo:**

```bash
# 1. Crie uma branch para a sua entrega
git checkout -b estudo-dirigido-semana05

# 2. Faça seu trabalho e commite
git add semana05/estudo_dirigido/respostas.md
git commit -m "docs: estudo dirigido semana 5 — condicionais"

# 3. Envie a branch para o GitHub
git push -u origin estudo-dirigido-semana05
```

Depois, no GitHub:
- Acesse o repositório
- Clique em **Compare & pull request**
- Escreva uma descrição do que foi feito
- Clique em **Create pull request**

O professor (ou colega revisor) analisa, comenta e aprova o merge.

---

## 10. Autenticação — resolvendo problemas comuns

### Erro: "Password authentication is not supported"

O GitHub não aceita mais senha simples. Use token ou SSH.

**Solução com token (HTTPS):**

```bash
# 1. Gere um token em: https://github.com/settings/tokens
#    (Settings → Personal access tokens → Tokens classic → Generate new token)
#    Marque o escopo "repo" e copie o token gerado

# 2. Configure o Git para salvar as credenciais
git config --global credential.helper store

# 3. No próximo push, quando pedir senha, cole o token (não a senha da conta)
git push
```

**Solução com SSH (recomendado para uso contínuo):**

```bash
# 1. Gerar par de chaves SSH
ssh-keygen -t ed25519 -C "seu@email.com"
# Pressione Enter em tudo para aceitar os padrões

# 2. Copiar a chave pública
cat ~/.ssh/id_ed25519.pub
# Cole o resultado em: GitHub → Settings → SSH and GPG keys → New SSH key

# 3. Testar a conexão
ssh -T git@github.com
# Resposta esperada: "Hi username! You've successfully authenticated..."

# 4. Trocar a URL do repositório de HTTPS para SSH
git remote set-url origin git@github.com:usuario/APC-2026-1.git
```

### Múltiplas contas GitHub na mesma máquina

```bash
# Gerar uma segunda chave com nome diferente
ssh-keygen -t ed25519 -C "conta2@email.com"
# Salvar como: ~/.ssh/id_ed25519_conta2

# Editar ~/.ssh/config
nano ~/.ssh/config
```

Conteúdo do arquivo `~/.ssh/config`:

```
# Conta principal
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519

# Segunda conta (ex: conta da UnB)
Host github-unb
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_conta2
```

```bash
# Usar o alias no repositório da segunda conta
git remote set-url origin git@github-unb:usuario_unb/APC-2026-1.git

# Testar cada conta
ssh -T git@github.com
ssh -T git@github-unb
```

### SSH bloqueado pela rede (porta 22 fechada)

```bash
# Testar SSH na porta 443 (geralmente aberta)
ssh -T -p 443 git@ssh.github.com

# Se funcionar, adicionar ao ~/.ssh/config:
# Host github.com
#   HostName ssh.github.com
#   User git
#   Port 443
#   IdentityFile ~/.ssh/id_ed25519
```

Se a porta 443 também estiver bloqueada (redes muito restritivas), use HTTPS com token — funciona em qualquer rede.

---

## 11. GitHub Pages — publicar sua página pessoal

```bash
# Criar o arquivo da página na raiz do repositório
touch index.html

# Editar com conteúdo básico, commitar e enviar
git add index.html
git commit -m "feat: página pessoal inicial com GitHub Pages"
git push
```

No GitHub:
- Acesse o repositório → **Settings → Pages**
- Em "Source", selecione **Deploy from a branch**
- Branch: `main`, pasta: `/ (root)`
- Salve — em alguns minutos sua página estará em:
  `https://usuario.github.io/APC-2026-1/`

---

## 12. Estrutura do repositório da disciplina

```
APC-2026-1/
├── README.md                  ← apresentação pessoal + lista de projetos
├── semana02/
│   ├── robo_algoritmos.md     ← descrição do simulador OctoStudio
│   └── fluxograma.png
├── semana03/
│   ├── simulador_cpu.md
│   └── calculadora_octostudio.png
├── semana09/
│   └── calculadora.py         ← primeira reimplementação em Python
├── semana11/
│   └── banco_dados_saeb.py
├── semana12/
│   └── agenda_contatos.py
├── semana14/
│   └── analisador_saeb.py
├── projeto_final/
│   ├── README.md
│   ├── proposta_pedagogica.md
│   └── src/
└── index.html                 ← GitHub Pages
```

---

## 13. Comandos de emergência

```bash
# "Perdi tudo, quero voltar ao último commit"
git checkout -- .

# "Fiz push de algo errado, quero desfazer publicamente"
git revert HEAD
git push

# "Quero ver o que tinha num arquivo em um commit antigo"
git show a3f9c12:semana03/calculadora.py

# "Quero recuperar um arquivo deletado"
git checkout HEAD -- arquivo_deletado.py

# "Meu repositório local está diferente do GitHub e o push está dando erro"
git pull --rebase
git push
```

---

## Resumo visual do fluxo

```
Arquivos no disco
      │
      │  git add
      ▼
Staging area (preparação)
      │
      │  git commit -m "mensagem"
      ▼
Repositório local (histórico)
      │
      │  git push
      ▼
GitHub (repositório remoto)
      │
      │  git pull
      ▼
Repositório local atualizado
```

---

*APC 2026/1 — Licenciatura em Computação — UnB*
*Atualizado em 16/03/2026*
