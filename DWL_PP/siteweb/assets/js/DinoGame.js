const game = document.getElementById("gameContainer");
  const dino = document.getElementById("dino");
  const scoreText = document.getElementById("score");
  const message = document.getElementById("message");
  const ground = document.getElementById("ground");
  const clouds = document.getElementById("clouds");

  let gameWidth = game.offsetWidth;

  let gravity = 0.72;
  let jumpPower = -14;

  let velocityY = 0;
  let dinoY = 0;
  let isJumping = false;

  let obstacles = [];
  let score = 0;
  let speed = 7;
  let spawnTimer = 0;

  let gameRunning = false;
  let gameOver = false;
  let animationFrame = null;

  function resize(){
      gameWidth = game.offsetWidth;
  }
  window.addEventListener("resize", resize);

  function createCloud(){
      if(!gameRunning) return;

      const cloud = document.createElement("div");
      cloud.className = "cloud";
      cloud.style.left = gameWidth + "px";
      cloud.style.top = Math.random() * 40 + "px";
      cloud.speed = 1 + Math.random() * 1.5;

      clouds.appendChild(cloud);
  }

  setInterval(createCloud, 2200);

  function moveClouds(){
      const all = document.querySelectorAll(".cloud");

      all.forEach(c=>{
          c.style.left = (parseFloat(c.style.left) - c.speed) + "px";

          if(parseFloat(c.style.left) < -100){
              c.remove();
          }
      });
  }

  function jump(){
      if(!gameRunning) return;

      if(!isJumping){
          velocityY = jumpPower;
          isJumping = true;
      }
  }

  document.addEventListener("keydown",(e)=>{

      if(e.code === "Space" || e.code === "ArrowUp"){

          e.preventDefault();

          if(gameOver){
              startGame();
              return;
          }

          if(!gameRunning){
              startGame();
              return;
          }

          jump();
      }

  });

  document.addEventListener("click",()=>{
      if(gameOver){
          startGame();
          return;
      }

      if(!gameRunning){
          startGame();
          return;
      }

      jump();
  });

  function createObstacle(){

      const obs = document.createElement("div");
      obs.className = "obstacle";

      const h = 35 + Math.random() * 25;

      obs.style.height = h + "px";
      obs.style.left = gameWidth + "px";

      game.appendChild(obs);

      obstacles.push({
          el: obs,
          x: gameWidth,
          w: 28,
          h: h
      });
  }

  function updateObstacles(){

      spawnTimer--;

      if(spawnTimer <= 0){
          createObstacle();
          spawnTimer = 70 + Math.random() * 50;
      }

      for(let i = obstacles.length - 1; i >= 0; i--){

          let o = obstacles[i];

          o.x -= speed;
          o.el.style.left = o.x + "px";

          if(o.x < -60){
              o.el.remove();
              obstacles.splice(i,1);
              continue;
          }

          if(checkCollision(o)){
              endGame();
              return; /* STOP direct */
          }
      }
  }

  function checkCollision(o){
      const scale = 2; // DOIT ÊTRE LA MÊME VALEUR QUE TON transform: scale(...) DANS LE CSS

      const dinoX = 70;
      // On multiplie la taille de base par l'échelle pour adapter la hitbox
      const dinoW = 48 * scale; 
      const dinoH = 52 * scale;
      const dinoBottom = dinoY;

      // Ajustement des marges internes (les 8 pixels de tolérance grandissent aussi)
      const hit =
          dinoX + dinoW - (8 * scale) > o.x &&
          dinoX + (8 * scale) < o.x + o.w &&
          dinoBottom < o.h;

      return hit;
  }

  function updateDino(){

      velocityY += gravity;
      dinoY -= velocityY;

      if(dinoY < 0){
          dinoY = 0;
          velocityY = 0;
          isJumping = false;
      }

      dino.style.bottom = (4 + dinoY) + "px";

      // const leg1 = dino.querySelector(".leg1");
      // const leg2 = dino.querySelector(".leg2");

      // if(!isJumping && gameRunning){

      //     let t = Date.now() / 80;

      //     leg1.style.height = (14 + Math.sin(t) * 6) + "px";
      //     leg2.style.height = (14 - Math.sin(t) * 6) + "px";
      // }
  }

  function updateGround(){

      let x = parseFloat(ground.dataset.x || 0);

      x -= speed;

      if(x <= -gameWidth){
          x = 0;
      }

      ground.dataset.x = x;
      ground.style.transform = `translateX(${x}px)`;
  }

  function updateScore(){

      score += 0.12;

      scoreText.textContent =
          Math.floor(score).toString().padStart(5,"0");

      if(Math.floor(score) % 100 === 0){
          speed += 0.002;
      }
  }

  function gameLoop(){

      if(!gameRunning) return;

      updateDino();
      updateObstacles();

      if(!gameRunning) return; /* sécurité collision */

      updateGround();
      updateScore();
      moveClouds();

      animationFrame = requestAnimationFrame(gameLoop);
  }

  function clearGame(){

      obstacles.forEach(o=>o.el.remove());
      obstacles = [];
  }

  function startGame(){

      cancelAnimationFrame(animationFrame);

      clearGame();

      score = 0;
      speed = 7;
      spawnTimer = 80;

      dinoY = 0;
      velocityY = 0;
      isJumping = false;

      dino.style.bottom = "4px";
      dino.className = "state-run";
      gameRunning = true;
      gameOver = false;

      message.style.display = "none";

      gameLoop();
  }

  function endGame(){
      gameRunning = false;
      gameOver = true;

      // --> AJOUTE CETTE LIGNE : On déclenche l'animation de Game Over
      dino.className = "state-dead";

      cancelAnimationFrame(animationFrame);

      message.innerHTML = `
          GAME OVER
          <div id="sub">
              Score : ${Math.floor(score)}<br>
              Appuie sur ESPACE pour rejouer
          </div>
      `;

      message.style.display = "block";
  }