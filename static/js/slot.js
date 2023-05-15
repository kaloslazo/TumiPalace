// ===: ACTIONS :===
let btnControlIncrease = document.getElementById("controlIncrease");
let btnControlDecrease = document.getElementById("controlDecrease");
const btnSpin = document.getElementById("btnSpin");
const rouletteMainLeft = document.getElementById("rouletteMainLeft");
const rouletteMainMiddle = document.getElementById("rouletteMainMiddle");
const rouletteMainRight = document.getElementById("rouletteMainRight");

// ===: SALARY :===
let userBank = document.getElementById("userBank");
let usrBet = document.getElementById("bankBet");
let usrBetVariable = 0;
let usrBankVariable = 1580.25;


// ===: CONTROL :===
let arrImages = ["logo1.jpeg", "logo2.jpeg", "logo3.jpeg", "logo4.jpeg"];
let arrMultiplies = [2, 4, 6, 8];
let timeRebuild = 5;

// Handle the spin animation of a slot
function handleSpinAnimation(idx) {
  let tempSpinnedVal = [];
  for (let i = 0; i < 3; i++) {
    if (i != idx) {
      tempSpinnedVal.push(i);
    }
  }
  // Shuffle the array of images
  let shuffledArr = tempSpinnedVal
    .map((value) => ({ value, sort: Math.random() }))
    .sort((a, b) => a.sort - b.sort)
    .map(({ value }) => value);
  // Display the images in the slot
  wrapperSlotsResults[idx].innerHTML = `
    <img src="static/img/slotsGame/${arrImages[shuffledArr[0]]}" alt="">
    <img src="static/img/slotsGame/${arrImages[spinnedVal[idx]]}" alt="">
    <img src="static/img/slotsGame/${arrImages[shuffledArr[1]]}" alt="">
  `;
  console.log(spinnedVal);
  // Set a timer to reset the animation after a delay
  let timer = setInterval(() => {
    timeRebuild--;
    if (timeRebuild === 0) {
      clearInterval(timer);
      resetAnimation();
    }
  }, 1000);
}

// Get a random value for a slot
function getRandomVal() {
  return Math.floor(Math.random() * arrMultiplies.length);
}

// Spin all the slots and get their values
function spinSlots() {
  spinnedVal = [getRandomVal(), getRandomVal(), getRandomVal()];
}

// Update the bet
function updateBankBet() {
    usrBet.textContent = usrBetVariable;
  }
  
  // Update the user bank
  function updateUsrBank() {
    // Check if the user won
    if (spinnedVal.every((val, i, arr) => val === arr[0])) {
      // Add the earnings to the bank
      usrBankVariable = usrBankVariable + usrBetPossible;
      // Reset the bet and the possible earnings
      usrBetVariable = 0;
      usrBetPossible = 0;
      updateBankBet();
    }
    // Display the bank
    userBank.innerHTML = usrBankVariable;
  }
  
  // Perform the control action
  function controlAction() {
    updateUsrBank();
    updateBankBet();
  }

  
  btnSpin.addEventListener("click", function onClick(e) {
    const spinSound = document.getElementById("spin");
  
    function playSpinSound() {
      spinSound.currentTime = 0;
      spinSound.play();
    }
  
    // Check if the user has enough balance
    if (usrBankVariable > 0 && usrBetVariable > 0){
      // Add a spinning animation to the button
      btnSpin.classList.add("anmSpinner");
      // Spin the slots and get their values
      spinSlots();
      // Update the bet and subtract it from the bank
      updateBankBet();
      usrBankVariable = usrBankVariable - usrBetVariable;
      // Update the bank
      updateUsrBank();
      // Play the spin sound
      playSpinSound();
      //
      console.log("SALDO:", usrBankVariable);
    } else {
      console.log("SALDO INSUFICIENTE");
    }
  });
  
  // Listen for the increase button click
  btnControlIncrease.addEventListener("click", function onCLick(e) {
    // Increase the bet by 5
    usrBetVariable = usrBetVariable + 5;
    // Perform the control action
    controlAction();
  });
  
  // Listen for the decrease button click
  btnControlDecrease.addEventListener("click", function onCLick(e) {
    // Check if the bet is positive
    if (usrBetVariable > 0) {
      // Decrease the bet by 5
      usrBetVariable = usrBetVariable - 5;
      // Perform the control action
      controlAction();
    }
  });
  

  //GIANKI SPIN
  document.addEventListener("DOMContentLoaded", () => {
    function getRandomNumber() {
      return Math.floor(Math.random() * 4) + 1;
    }
  
    function resetButtonAnimation() {
      btnSpin.classList.remove("anmSpinner");
    }
  
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
        }, 5000);
      }
    }
  
    btnSpin.addEventListener("click", rotateReels);
  });
  
  // ===: EXECUTION :===
  updateUsrBank();
  controlAction();