var fundo = createSprite(200,200);
fundo.setAnimation("cave_1");
// fundo.setAnimation("space_1");
// background()
// Create your variables here

// Create your sprites here
var nave = createSprite(60, 350, 50,50);
nave.setAnimation("playerShip2_red_1");
// nave.debug = true;
nave.scale = 0.6;
// nave.velocityX = 0.3;

var coin = createSprite(200, 200, 5, 5);
coin.setAnimation("coin_gold_1");
coin.scale = 0.3;
coin.setCollider("circle");

var vida1 = createSprite(30, 45, 20,20);
vida1.setAnimation("retro_red_heart_1");
vida1.scale = 0.15;

var vida2 = createSprite(55, 45, 20,20);
vida2.setAnimation("retro_red_heart_1");
vida2.scale = 0.15;

var vida3 = createSprite(80, 45, 20,20);
vida3.setAnimation("retro_red_heart_1");
vida3.scale = 0.15;

var vida4 = createSprite(105, 45, 20,20);
vida4.setAnimation("retro_red_heart_1");
vida4.scale = 0.15;

var vida5 = createSprite(130, 45, 20,20);
vida5.setAnimation("retro_red_heart_1");
vida5.scale = 0.15;

var tiro = createSprite(nave.x, nave.y, 5, 5);
tiro.setAnimation("target_white_1");
tiro.scale = 0.1;

var bomb1 = createSprite(randomNumber(0, 400), 0);
bomb1.setAnimation("pieceBlack_border11_1");
// bomb1.debug=true;
bomb1.setCollider("circle",0,0,20);
bomb1.scale = 0.3;
bomb1.velocityY = 3;
var bomb1_ativa = true;
// bomb1.velocityY = 1;

var bomb2 = createSprite(randomNumber(0, 400), 0);
bomb2.setAnimation("pieceBlack_border11_1");
bomb2.velocityY = 1;
// bomb2.debug=true;
bomb2.setCollider("circle",0,0,20);
bomb2.scale = 0.3;
bomb2.velocityY = 3;
var bomb2_ativa = true;


var bomb3 = createSprite(randomNumber(0, 400), 0);
bomb3.setAnimation("pieceBlack_border11_1");
bomb3.velocityY = 1;
bomb3.setCollider("circle",0,0,20);
bomb3.scale = 0.3;
bomb3.velocityY = 3;
var bomb3_ativa = true;

var bomb4 = createSprite(randomNumber(0, 400), 0);
bomb4.setAnimation("pieceBlack_border11_1");
bomb4.velocityY = 1;
bomb4.setCollider("circle",0,0,20);
bomb4.scale = 0.3;
bomb4.velocityY = 3;
var bomb4_ativa = true;

// line(380,350,380,380);
// 
// var bombas = [bomb1, bomb2, bomb3, bomb4];
// function ativa(){
//   return true;
// }
function bomba(){
  // bomb(num.setAnimation("pieceBlack_border11_1");
  // if(bombas[num].y >= 400){
  //   bomb1_ativa = true;
  //   bombas[num].setAnimation("pieceBlack_border11_1");
  //   bombas[num].y = 1;
  //   bombas[num].x = randomNumber(0, 400);
  //   bombas[num].velocityY = randomNumber(1, 20);
  // }
  
  if(bomb1.y >= 400){
    bomb1.setAnimation("pieceBlack_border11_1");
    bomb1.y = 1;
    bomb1.x = randomNumber(0, 400);
    bomb1.velocityY = randomNumber(1, 20);
    bomb1_ativa = true;
  }
  if(bomb2.y >= 400){
    bomb2.setAnimation("pieceBlack_border11_1");
    bomb2.y = 1;
    bomb2.x = randomNumber(0, 400);
    bomb2.velocityY = randomNumber(1, 20);
    bomb2_ativa = true;
  }
  if(bomb3.y >= 400){
    bomb3.setAnimation("pieceBlack_border11_1");
    bomb3.y = 1;
    bomb3.x = randomNumber(0, 400);
    bomb3.velocityY = randomNumber(1, 20);
    bomb3_ativa = true;
  }
  if(bomb4.y >= 400){
    bomb4.setAnimation("pieceBlack_border11_1");
    bomb4.y = 1;
    bomb4.x = randomNumber(0, 400);
    bomb4.velocityY = randomNumber(1, 20);
    bomb4_ativa = true;
  }
}

var vidas = 5;
function vida(){
    // if ((nave.isTouching(bomb1)) || (nave.isTouching(bomb2)) || (nave.isTouching(bomb3)) || (nave.isTouching(bomb4))){
    //     vidas = vidas - 1;
    // }    
    //     console.log(("Tocou"));
    // }
    // if (vidas == 5){
    //     vida5.setAnimation("retro_empty_heart_1");
    // }
    if (nave.isTouching(bomb1) && bomb1_ativa == true) {
        vidas = vidas - 1;
        bomb1_ativa = false;
        // console.log(("Tocou bomb1"));
    }
    if (nave.isTouching(bomb2) && bomb2_ativa == true) {
        vidas = vidas - 1;
        bomb2_ativa = false;
        // console.log(("Tocou bomb2"));
    }
    if(nave.isTouching(bomb3) && bomb3_ativa == true) {
        vidas = vidas - 1;
        bomb3_ativa = false;
        // console.log(("Tocou bomb3"));

    }
    if(nave.isTouching(bomb4) && bomb4_ativa == true){
        vidas = vidas - 1;
        bomb4_ativa = false;
        // console.log(("Tocou bomb4"));
    }
    if (vidas == 4){
        vida5.setAnimation("semvida");
    }
    if (vidas == 3){
        vida4.setAnimation("semvida");
    }
    if (vidas == 2){
        vida3.setAnimation("semvida");
    }
    if (vidas == 1){
        vida2.setAnimation("semvida");
    }
    // if (vidas == 0){
    //     vida1.setAnimation("semvida");
    //     endgame();
    // }
    // console.log(bomb1_ativa);

    // console.log("bomb1: " + bomb1_ativa, "bomb2: " + bomb2_ativa, "bomb3: " + bomb3_ativa, "bomb4: " + bomb4_ativa);
    // console.log(vidas);
}

function explode_bomba(){
    if (tiro.isTouching(bomb1) ){
        bomb1.setAnimation("explosao");
        bomb1_ativa = false;
        // console.log("bateu");
    }
    if (tiro.isTouching(bomb2)){
        bomb2.setAnimation("explosao");
        bomb2_ativa = false;
    }
    if (tiro.isTouching(bomb3)){
        bomb3.setAnimation("explosao");
        bomb3_ativa = false;
    }
    if (tiro.isTouching(bomb4)){
        bomb4.setAnimation("explosao");
        bomb4_ativa = false;
    }
}

function movimento_coin(){
  coin.velocityY = 3;
  if (coin.y > 400){
    coin.y = 0;
    coin.x = randomNumber(0, 400);
  }
}

function movimento_nave(){
  // nave.x = World.mouseX;
  // if (keyDown("right")){
  //   nave.velocityX = nave.velocityX + 0.3;
  // }
  // if (keyDown("left")){
  //   nave.velocityX = nave.velocityX - 0.3;
  // }
  // if ((nave.x > -20) && (nave.x < 420)) {
    if (keyDown("right") && (nave.x < 420)){
        nave.x = nave.x + 20;
    }
    if (keyDown("left") && (nave.x > -20)){
        nave.x = nave.x - 20;
    }
// }
}

function movimento_tiro(){
  tiro.velocityY = -16;
  if (tiro.y < 0){
    tiro.y = nave.y;
    tiro.x = nave.x;
  }
}

var score = 0;
function placar(){
  if(nave.isTouching(coin)){
    score += 1;
    coin.y = 0;
    coin.x = randomNumber(0, 400);
  }
  textSize(16);
  fill("white");
  text("Coins: " + score, 10, 25);
  noFill();
}

function draw() {
  // bomb1_ativa = true;
  bomba();
  // bomba(1);
  movimento_nave();  
  movimento_coin();
  movimento_tiro();
  explode_bomba();
   
  // drawSprites(vida);
  drawSprites();
  vida();
  placar();
  if (vidas == 0)
  {textSize(16);
  fill("white");
  text("GAME OVER!!", 200, 200);
  noFill();}
}

// function endgame(){
//   background("black");
//   textSize(16);
//   fill("white");
//   text("GAME OVER!!", 200, 200);
//   noFill();
// }
// Create your functions here
