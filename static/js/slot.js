let btnControlIncrease = document.getElementById("controlIncrease");
let btnControlDecrease = document.getElementById("controlDecrease");
const btnSpin = document.getElementById("btnSpin");
const rouletteMainLeft = document.getElementById("rouletteLeftMid");
const rouletteMainMiddle = document.getElementById("rouletteMiddleMid");
const rouletteMainRight = document.getElementById("rouletteRightMid");
const rouletteMainLeftUP = document.getElementById("rouletteLeftUp");
const rouletteMainMiddleUP = document.getElementById("rouletteMiddleUp");
const rouletteMainRightUP = document.getElementById("rouletteRightUp");
const rouletteMainLeftDown = document.getElementById("rouletteLeftDown");
const rouletteMainMiddleDown = document.getElementById("rouletteMiddleDown");
const rouletteMainRightDown = document.getElementById("rouletteRightDown");
const resultMessage = document.getElementById("resultMessage")

let userBank = document.getElementById("userBank");
let usrBet = document.getElementById("bankBet");
let usrBetVariable = 0;
let usrBankVariable = 1000;
userBank.textContent = usrBankVariable;


// Ver si Ganó
function checkWin() {
  const leftImage = rouletteMainLeft.querySelector("img").getAttribute("src");
  const middleImage = rouletteMainMiddle.querySelector("img").getAttribute("src");
  const rightImage = rouletteMainRight.querySelector("img").getAttribute("src");

  if (leftImage === middleImage && middleImage === rightImage) {
    let winnings;
    const winSound = document.getElementById("win");
    winSound.currentTime = 0;
    winSound.play();

    if (leftImage.includes("logo2") && middleImage.includes("logo2") && rightImage.includes("logo2")) {
      winnings = usrBetVariable * 2;
    } else if (leftImage.includes("logo4") && middleImage.includes("logo4") && rightImage.includes("logo4")) {
      winnings = usrBetVariable * 4;
    } else if (leftImage.includes("logo1") && middleImage.includes("logo1") && rightImage.includes("logo1")) {
      winnings = usrBetVariable * 6;
    } else if (leftImage.includes("logo3") && middleImage.includes("logo3") && rightImage.includes("logo3")) {
      winnings = usrBetVariable * 8;
    } else {
      return;
    }

    usrBankVariable += winnings;
    userBank.textContent = usrBankVariable;
    const message = "¡Ganaste! Tus ganancias son: " + winnings;
    console.log(message);
    resultMessage.textContent = message; 

    setTimeout(function() {
      resultMessage.textContent = "";
    }, 1000);
  } 
}



  // Llamada para el boton de aumento
    btnControlIncrease.addEventListener("click", function onCLick(e) {
      usrBetVariable = usrBetVariable + 5;
      usrBet.textContent = usrBetVariable;
    });
    
  // Llamada para el boton de disminuir
    btnControlDecrease.addEventListener("click", function onCLick(e) {
      if (usrBetVariable > 0){
        usrBetVariable = usrBetVariable - 5;
        
        usrBet.textContent = usrBetVariable;
      }
    });  

  // LLamada para el boton de girar
    btnSpin.addEventListener("click", function onClick(e) {
      if (usrBankVariable > 0 && usrBetVariable > 0 && usrBankVariable>=usrBetVariable){
        btnSpin.classList.add("anmSpinner");
        const spinSound = document.getElementById("spin");
        spinSound.currentTime = 0;
        spinSound.play();
        rotateReels();
        usrBankVariable = usrBankVariable - usrBetVariable;
        userBank.textContent = usrBankVariable;
        console.log("SALDO:", usrBankVariable);
      } else {
        console.log("SALDO INSUFICIENTE");
        resultMessage.textContent = "SALDO INSUFICIENTE";

        setTimeout(function() {
          resultMessage.textContent = "";
        }, 1000);
      }
    });
    
  // ===: Girar La ruleta :===
    function getRandomNumber() {return Math.floor(Math.random() * 4) + 1;}
    function resetButtonAnimation() {btnSpin.classList.remove("anmSpinner");}
    function rotateReels() {
      if (usrBankVariable > 0 && usrBetVariable > 0 && usrBankVariable>=usrBetVariable) {
        btnSpin.disabled = true;
        btnControlDecrease.disabled=true;
        btnControlIncrease.disabled=true;
        const resultSound = document.getElementById("result");
    
        function playResultSound() {
          resultSound.currentTime = 0;
          resultSound.play();
        }
    
        const interval = setInterval(() => {
          const newRandomNumberLeft = getRandomNumber();
          const newRandomNumberMiddle = getRandomNumber();
          const newRandomNumberRight = getRandomNumber();
          const newRandomNumberLeftUp = getRandomNumber();
          const newRandomNumberLeftDown = getRandomNumber();
          const newRandomNumberMiddleUp = getRandomNumber();
          const newRandomNumberMiddleDown = getRandomNumber();
          const newRandomNumberRightUp = getRandomNumber();
          const newRandomNumberRightDown = getRandomNumber();


          rouletteMainLeftUP.innerHTML = `
              <img src="static/img/slotsGame/logo${newRandomNumberLeftUp}.jpeg" alt="">
          `;
          rouletteMainMiddleUP.innerHTML = `
              <img src="static/img/slotsGame/logo${newRandomNumberMiddleUp}.jpeg" alt="">
          `;
          rouletteMainRightUP.innerHTML = `
              <img src="static/img/slotsGame/logo${newRandomNumberRightUp}.jpeg" alt="">
          `;

          rouletteMainLeft.innerHTML = `
              <img src="static/img/slotsGame/logo${newRandomNumberLeft}.jpeg" alt="">
          `;
          rouletteMainMiddle.innerHTML = `
              <img src="static/img/slotsGame/logo${newRandomNumberMiddle}.jpeg" alt="">
          `;
          rouletteMainRight.innerHTML = `
              <img src="static/img/slotsGame/logo${newRandomNumberRight}.jpeg" alt="">
          `;

          rouletteMainLeftDown.innerHTML = `
              <img src="static/img/slotsGame/logo${newRandomNumberLeftDown}.jpeg" alt="">
          `;
          rouletteMainMiddleDown.innerHTML = `
              <img src="static/img/slotsGame/logo${newRandomNumberMiddleDown}.jpeg" alt="">
          `;
          rouletteMainRightDown.innerHTML = `
              <img src="static/img/slotsGame/logo${newRandomNumberRightDown}.jpeg" alt="">
          `;
        }, 200);
    
        setTimeout(() => {
          clearInterval(interval);
          playResultSound();
          btnSpin.disabled = false;
          btnControlDecrease.disabled=false;
          btnControlIncrease.disabled=false;
          resetButtonAnimation(); 
          checkWin();
        }, 5000);
      }
    }
    document.addEventListener("DOMContentLoaded", () => {
    btnSpin.addEventListener("click", rotateReels);
    });
  ;
    