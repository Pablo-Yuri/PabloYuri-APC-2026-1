// GAME SETUP
// create player, target, and obstacles
var pontos = 0;

var player = createSprite(200, 100);
player.setAnimation("fly_bot");
player.scale = 0.5;
player.debug = true;

var obstacle1 = createSprite(300, -10);
obstacle1.setAnimation("rock");
obstacle1.velocityY = 4;
obstacle1.debug = true;

var obstacle2 = createSprite(-10, 150);
obstacle2.setAnimation("rock");
obstacle2.velocityX = 5;
obstacle2.debug = true;

var coin = createSprite(randomNumber(0, 400), randomNumber(0, 400));
coin.setAnimation("coin");
coin.setCollider("circle");
coin.debug= true;

function draw() {
  background("lightblue");
  player.setAnimation("fly_bot_1");

  // FALLING
  player.velocityY = player.velocityY + 0.3;
  
  // LOOPING
  if (obstacle1.y < 0 || obstacle1.y > 400){
    obstacle1.x = randomNumber(50, 350);
    obstacle1.y = 0;
  }
  if (obstacle2.x < 0 || obstacle2.x > 400){
    obstacle2.y = randomNumber(50, 350);
    obstacle2.x = 0;
  }
  
  
  // PLAYER CONTROLS
  // change the y velocity when the user clicks "up"
  if (keyDown("up")){
    player.velocityY = player.velocityY - 0.6;
  }
  
  // decrease the x velocity when user clicks "left"
  if (keyDown("left")){
    player.velocityX = player.velocityX - 0.3;
  }
  
  // increase the y velocity when the user clicks "right"
  if (keyDown("right")){
    player.velocityX = player.velocityX + 0.3;
  }
  
  // SPRITE INTERACTIONS
  // reset the coin when the player touches it
  if (coin.isTouching(player)){
    pontos += 1;
    console.log("tocando");
    coin.visible=false;
    coin = createSprite(randomNumber(0, 400), randomNumber(0, 400));
    coin.setAnimation("coin");
    coin.setCollider("circle");
    // coin.debug= true;
  }
  
  // make the obstacles push the player
  if (player.isTouching(obstacle1)){
    player.collide(obstacle1);
  }
  if (player.isTouching(obstacle2)){
    player.collide(obstacle2);
  }
  
  
  // DRAW SPRITES
  drawSprites();
  
  // GAME OVER
  if (player.x < -50 || player.x > 450 || player.y < -50 || player.y > 450) {
    background("black");
    textSize(50);
    fill("green");
    text("Game Over!", 50, 200);
  }
  textSize(16);
  text("Pontos: ", 20, 20);
  text(pontos, 80, 20);
  
}
