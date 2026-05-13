# Semana 7

Continuação das atividades no Code.org, agora com foco em condicionais, entrada por teclado e movimento do mouse.

Foram concluídos os módulos 10, 11 e 12.

## Visão Geral dos Arquivos

- img_m10/balloon.mp4: vídeo do balão crescendo até estourar.
- img_m11/mosca.mp4: vídeo com a mosca se movendo pelas setas do teclado.
- img_m12/abelhas.mp4: vídeo com abelhas seguindo o mouse.

---

## Módulo 13 - Velocidade

### Objetivo

Usar expressões condicionais para criar eventos que acontecem quando uma propriedade do sprite atinge determinado valor.

### Exemplo

Fazer o balão crescer até estourar e trocar para a animação de estouro quando a escala ficar grande demais.

```javascript
// Cria o balão no centro da tela e inicia com escala pequena
var balloon = createSprite(200, 200);
balloon.setAnimation("balloon");
balloon.scale = 0.1;

// Cria o sprite do estouro, que começa invisível
var pop = createSprite(200, 200);
pop.setAnimation("pop");

function draw() {
  // Fundo da cena
  background("white");

  // Faz o balão crescer a cada quadro
  balloon.scale = balloon.scale + 0.006;

  // Mantém o estouro oculto até o momento da colisão visual
  pop.visible = false;

  // Quando o balão fica grande demais, troca a visibilidade dos sprites
  if (balloon.scale > 0.8) {
    balloon.visible = false;
    pop.visible = true;
  }

  // Desenha os sprites na tela
  drawSprites();
}
```

### Resultado

<div align="center">
  <video controls width="30%">
    <source src="./img_m10/balloon.mp4" type="video/mp4">
  </video>
  <figcaption>Vídeo obtido na atividade.</figcaption>
</div>

---

## Módulo 14 - Detecção de Colisões

### Objetivo

Controlar sprites com as setas do teclado e trocar a animação conforme a direção do movimento.

### Exemplo

Movimentar um inseto com as setas e alterar sua animação de acordo com a direção pressionada.

```javascript
// Cria o sprite da mosca/inseto com a animação inicial
var bug = createSprite(200, 200);
bug.setAnimation("fly_L");

function draw() {
  // Fundo da cena
  background("white");

  // Move para cima e troca a animação correspondente
  if (keyDown("up")) {
    bug.y = bug.y - 5;
    bug.setAnimation("fly_up");
  }

  // Move para baixo e troca a animação correspondente
  if (keyDown("down")) {
    bug.y = bug.y + 5;
    bug.setAnimation("fly_down");
  }

  // Move para a esquerda e troca a animação correspondente
  if (keyDown("left")) {
    bug.x = bug.x - 5;
    bug.setAnimation("fly_L");
  }

  // Move para a direita e troca a animação correspondente
  if (keyDown("right")) {
    bug.x = bug.x + 5;
    bug.setAnimation("fly_R");
  }

  // Desenha a cena final
  drawSprites();
}
```

### Resultado

<div align="center">
  <video controls width="30%">
    <source src="./img_m11/mosca.mp4" type="video/mp4">
  </video>
  <figcaption>Vídeo obtido na atividade.</figcaption>
</div>

---

## Módulo 15 - Movimento Complexo de Sprites

### Objetivo

Fazer sprites acompanharem o mouse e variar um pouco a posição para criar um movimento mais natural.

### Exemplo

Criar três abelhas e atualizá-las a partir da posição do mouse, com pequenas variações aleatórias ao redor do cursor.

```javascript
// Cria três sprites de abelha
var bee = createSprite(200, 200, 50, 50);
bee.setAnimation("bee");

var bee2 = createSprite(200, 200, 50, 50);
bee2.setAnimation("bee");

var bee3 = createSprite(200, 200, 50, 50);
bee3.setAnimation("bee");

function draw() {
  // Fundo azul claro da cena
  background(rgb(144, 179, 217));

  // Faz cada abelha acompanhar o mouse com uma pequena variação aleatoria
  bee.x = randomNumber(World.mouseX - 50, World.mouseX + 50);
  bee.y = randomNumber(World.mouseY - 50, World.mouseY + 50);

  bee2.x = randomNumber(World.mouseX - 50, World.mouseX + 50);
  bee2.y = randomNumber(World.mouseY - 50, World.mouseY + 50);

  bee3.x = randomNumber(World.mouseX - 50, World.mouseX + 50);
  bee3.y = randomNumber(World.mouseY - 50, World.mouseY + 50);

  // Define a velocidade da animação e desenha os sprites
  World.frameRate = 10;
  drawSprites();
}
```

### Resultado

<div align="center">
  <video controls width="30%">
    <source src="./img_m12/abelhas.mp4" type="video/mp4">
  </video>
  <figcaption>Vídeo obtido na atividade.</figcaption>
</div>

---

