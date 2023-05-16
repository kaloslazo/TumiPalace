// ===: ACTIONS :===
let btnControlIncrease = document.getElementById("controlIncrease");
let btnControlDecrease = document.getElementById("controlDecrease");
const btnSpin = document.getElementById("btnSpin");
const rouletteMainLeft = document.getElementById("rouletteMainLeft");
const rouletteMainMiddle = document.getElementById("rouletteMainMiddle");
const rouletteMainRight = document.getElementById("rouletteMainRight");

// ===: BANK :===
let userBank = document.getElementById("userBank");
let usrBet = document.getElementById("bankBet");
let usrBetVariable = 0;
let usrBankVariable = 1000;
userBank.textContent = usrBankVariable;

// ===: Funciones :===

// Ver si Ganó
function checkWin() {
  const leftImage = rouletteMainLeft.querySelector("img").getAttribute("src");
  const middleImage = rouletteMainMiddle.querySelector("img").getAttribute("src");
  const rightImage = rouletteMainRight.querySelector("img").getAttribute("src");

  if (leftImage === middleImage && middleImage === rightImage) {
    // El jugador ganó
    let winnings;
    const winSound = document.getElementById("win");
        winSound.currentTime = 0;
        winSound.play();
    
    if (leftImage.includes("logo2")) {
      winnings = usrBetVariable * 2;
    } else if (leftImage.includes("logo4")) {
      winnings = usrBetVariable * 4;
    } else if (leftImage.includes("logo1")) {
      winnings = usrBetVariable * 6;
    } else if (leftImage.includes("logo3")) {
      winnings = usrBetVariable * 8;
    }

    usrBankVariable += winnings;
    // Mostrar el nuevo valor
    userBank.textContent = usrBankVariable;
    console.log("¡Ganaste! Tus ganancias son: " + winnings);
  } else {
    // El jugador perdió
    console.log("Perdiste. Inténtalo de nuevo.");
  }
}
  
  // Llamada para el boton de aumento
    btnControlIncrease.addEventListener("click", function onCLick(e) {
      // Incrementar en 5
      usrBetVariable = usrBetVariable + 5;
      // Mostrar el Nuevo Valor
      usrBet.textContent = usrBetVariable;
    });
    
  // Llamada para el boton de disminuir
    btnControlDecrease.addEventListener("click", function onCLick(e) {
      // Ver si la apuesta es mayor a 0
      if (usrBetVariable > 0) {
        // Restar en 5
        usrBetVariable = usrBetVariable - 5;
        // Mostrar el Nuevo Valor
        usrBet.textContent = usrBetVariable;
      }
    });  

  // LLamada para el boton de girar
    btnSpin.addEventListener("click", function onClick(e) {
      // Check if the user has enough balance
      if (usrBankVariable > 0 && usrBetVariable > 0){
        // Add a spinning animation to the button
        btnSpin.classList.add("anmSpinner");
        // Play the spin sound
        const spinSound = document.getElementById("spin");
        spinSound.currentTime = 0;
        spinSound.play();
        // Spin the slots and get their values
        rotateReels();
        // Update the bet and subtract it from the bank
        usrBankVariable = usrBankVariable - usrBetVariable;
        // Mostrar el nuevo valor
        userBank.textContent = usrBankVariable;
        // Update the bank
        console.log("SALDO:", usrBankVariable);
      } else {
        console.log("SALDO INSUFICIENTE");
      }
    });
    
  // ===: Girar La ruleta :===
    function getRandomNumber() {return Math.floor(Math.random() * 4) + 1;}
    function resetButtonAnimation() {btnSpin.classList.remove("anmSpinner");}
    function rotateReels() {
      if (usrBankVariable > 0 && usrBetVariable > 0) {
        btnSpin.disabled = true;
        const resultSound = document.getElementById("result");
    
        function playResultSound() {
          resultSound.currentTime = 0;
          resultSound.play();
        }
    
        const interval = setInterval(() => {
          const newRandomNumberLeft = getRandomNumber();
          const newRandomNumberMiddle = getRandomNumber();
          const newRandomNumberRight = getRandomNumber();
          rouletteMainLeft.innerHTML = `
            <div class="slotsResults">
              <img src="static/img/slotsGame/logo${newRandomNumberLeft}.jpeg" alt="">
            </div>
          `;
          rouletteMainMiddle.innerHTML = `
            <div class="slotsResults">
              <img src="static/img/slotsGame/logo${newRandomNumberMiddle}.jpeg" alt="">
            </div>
          `;
          rouletteMainRight.innerHTML = `
            <div class="slotsResults">
              <img src="static/img/slotsGame/logo${newRandomNumberRight}.jpeg" alt="">
            </div>
          `;
        }, 200);
    
        setTimeout(() => {
          clearInterval(interval);
          playResultSound();
          btnSpin.disabled = false;
          resetButtonAnimation(); // Reiniciar la animación del botón
          checkWin();
        }, 5000);
      }
    }
    document.addEventListener("DOMContentLoaded", () => {
    btnSpin.addEventListener("click", rotateReels);
    });
  ;
    