# Semana 6

Continuação das atividades no Code.org, agora com foco em textos, repetição, movimento e interação entre sprites.

Foram concluidos os modulos 7, 8 e 9.

## Visao Geral dos Arquivos

- img_m7/texto_aleatorio.png: cena gerada com elementos e cores aleatorias.
- img_m7/texto_original.png: referencia usada na atividade.
- img_m8/astronautas.png: cena com dois sprites em um cenario espacial.
- img_m9/peixes.png: cena com peixes e movimento controlado por teclado.

---

## Modulo 7 - Textos

### Objetivo

Mostrar como inserir texto na cena e combinar isso com formas e cores geradas no Code.org.

### Exemplo

Usar texto junto com uma cena colorida, mantendo a composicao visual parecida com a imagem de referencia.

```javascript
// Define o fundo azul da cena
background(rgb(5, 55, 255));

// Desenha circulos concêntricos com cores parcialmente aleatorias
fill(rgb(randomNumber(0, 255), randomNumber(0, 255), 255));
ellipse(200, 200, 400, 400);

fill(rgb(255, randomNumber(0, 255), 102));
ellipse(200, 200, 340, 340);

fill(rgb(randomNumber(0, 255), 255, 102));
ellipse(200, 200, 280, 280);

fill(rgb(178, randomNumber(0, 255), 102));
ellipse(200, 200, 220, 220);

fill(rgb(51, 153, randomNumber(0, 255)));
ellipse(200, 200, 160, 160);

fill(rgb(153, 153, randomNumber(0, 255)));
ellipse(200, 200, 100, 100);

fill(rgb(randomNumber(0, 255), randomNumber(0, 255), 255));
ellipse(200, 200, 40, 40);

// Desenha a base verde da cena
fill(rgb(25, 255, 0));
rect(0, 200, 400, 200);
```

### Resultado

<div align="center">
  <img src="./img_m7/m7.png" alt="Cena gerada de forma aleatoria" width="30%">
  <!-- <img src="./img_m7/texto_original.png" alt="Imagem de referencia da atividade" width="30%"> -->
  <!-- <figcaption>Da esquerda para a direita: resultado aleatorio e referencia.</figcaption> -->
</div>

---

## Modulo 8 - O laço de repeticao

### Objetivo

Usar repeticao e rotacao para animar sprites e criar uma cena espacial mais dinamica.

### Exemplo

Colocar dois sprites para dançar no espaco, alterar suas rotacoes e adicionar estrelas na cena.

```javascript
// Define a velocidade da execucao do desenho
World.frameRate = 10;

// Cria os sprites dos astronautas/aliens
var greenAlien = createSprite(100, 200);
greenAlien.setAnimation("greenAlien");

var pinkAlien = createSprite(300, 200);
pinkAlien.setAnimation("pinkAlien");

// Configura o desenho inicial
noStroke();
fill("white");

function draw() {
  // Fundo preto para simular o espaco
  background("black");

  // Estrelas desenhadas com posicoes aleatorias
  fill("yellow");
  ellipse(randomNumber(0, 400), randomNumber(0, 400), 5, 5);
  ellipse(randomNumber(0, 400), randomNumber(0, 400), 5, 5);
  noFill();
  ellipse(randomNumber(0, 400), randomNumber(0, 400), 5, 5);

  // Faz os sprites girarem levemente a cada quadro
  greenAlien.rotation = randomNumber(-4, 4);
  pinkAlien.rotation = randomNumber(-5, 5);

  // Desenha os sprites na tela
  drawSprites();

  // Escreve o texto da cena
  fill("white");
  textSize(20);
  text("Bora dançar!", 50, 140);
  text("Bora!", 250, 140);
}
```

### Resultado

<div align="center">
    <video controls width="30%">
        <source src="./img_m8/astro.mp4" type="video/mp4" alt="Cena com dois sprites no espaco" width="30%">
    </video>
  <!-- <img src="./img_m8/astronautas.png" alt="Cena com dois sprites no espaco" width="30%"> -->
  <figcaption>Video obtido na atividade.</figcaption>
</div>

---

## Modulo 9 - Movimento de Sprite

### Objetivo

Controlar o movimento de sprites com o teclado e criar elementos que se movem automaticamente.

### Exemplo

Movimentar peixes com a tecla esquerda e criar bolhas que sobem na tela ao longo do tempo.

```javascript
// Cria os peixes em posicoes aleatorias na vertical
var orangeFish = createSprite(400, randomNumber(50, 100));
orangeFish.setAnimation("orange_fish");

var blueFish = createSprite(300, randomNumber(50, 200));
blueFish.setAnimation("blue_fish");

var greenFish = createSprite(300, randomNumber(200, 300));
greenFish.setAnimation("green_fish");

// Controla a posicao das bolhas desenhadas manualmente
var posBubble = 400;

function draw() {
  // Fundo do mar
  background("navy");

  // Move os peixes para a esquerda quando a tecla estiver pressionada
  if (keyDown("left")) {
    orangeFish.x = orangeFish.x - 2;
    orangeFish.rotation = randomNumber(-1, 1);

    blueFish.x = blueFish.x - 3;
    blueFish.rotation = randomNumber(-1, 1);

    greenFish.x = greenFish.x - 1;
    greenFish.rotation = randomNumber(-1, 1);
  }

  // Desenha bolhas com pequenas variacoes verticais
  fill("white");
  ellipse(80, posBubble - 25, 30, 30);
  ellipse(120, posBubble, 30, 30);
  ellipse(180, posBubble - 50, 30, 30);
  ellipse(240, posBubble, 30, 30);
  ellipse(300, posBubble - 70, 30, 30);
  posBubble = posBubble - 1;
  noFill();

  // Desenha os sprites na tela
  drawSprites();
}
```

### Resultado

<div align="center">
    <video controls width="30%">
        <source src="./img_m9/peixes_nadando.mp4" type="video/mp4" alt="Cena com peixes e bolhas" width="30%">
    </video>
    <figcaption>Video obtido na atividade.</figcaption>
</div>

---

