//===: ACTIONS :===
let btnControlIncrease = document.getElementById("controlIncrease");
let btnControlDecrease = document.getElementById("controlDecrease");


//===: SALARY :===
let userBank = document.getElementById("userBank");
let bankPossibleEarned = document.getElementById("bankPossibleEarned");
let usrBet= document.getElementById("bankBet");
let usrBetVariable = 0;
let usrBetPossible = 0;
let usrBankVariable = 1580.25;


//===: Spin logic :===
let wrapperSlotsResults = document.getElementsByClassName("slotsResults");
let btnSpin = document.getElementById("btnSpin");
let spinnedVal = [0, 1, 2];


//===: CONTROL :===
let arrImages = ["logo1.jpeg", "logo2.jpeg", "logo3.jpeg", "logo4.jpeg"];
let arrMultiplies = [2, 4, 6, 8];
let timeRebuild = 5;

//===: FUNCTIONS :===
function resetAnimation(){
    wrapperSlotsResults[idx].innerHTML =  `
        <img src="static/img/slotsGame/logo2.jpeg" alt=""> 
        <img src="static/img/slotsGame/logo1.jpeg" alt=""> 
        <img src="static/img/slotsGame/logo4.jpeg" alt=""> 
    `;
};
function handleSpinAnimation(idx){
    let tempSpinnedVal = [];
    for(let i=0; i<3; i++){
        if(i != idx){
            tempSpinnedVal.push(i);
        };
    };
    let shuffledArr = tempSpinnedVal
    .map(value => ({ value, sort: Math.random() }))
    .sort((a, b) => a.sort - b.sort)
    .map(({ value }) => value);

    wrapperSlotsResults[idx].innerHTML =  `
        <img src="static/img/slotsGame/${arrImages[shuffledArr[0]]}" alt=""> 
        <img src="static/img/slotsGame/${arrImages[spinnedVal[idx]]}" alt=""> 
        <img src="static/img/slotsGame/${arrImages[shuffledArr[1]]}" alt=""> 
    `;
    console.log(spinnedVal);
    let timer = setInterval(() => {
        timeRebuild--
        if(timeRebuild = 0){
            clearInterval(timer);
            resetAnimation();
        };
    }, 1000);
};
function getRandomVal(){
    return Math.floor(Math.random() * (arrMultiplies.length));
};
function spinSlots(){
    spinnedVal = [getRandomVal(), getRandomVal(), getRandomVal()];
};
function updateBankBet(){
    usrBet.innerHTML = usrBetVariable;
};
function updateBankPossibleEarned(){
    usrBetPossible = usrBetVariable * arrMultiplies[((arrMultiplies.length)-1)];
    bankPossibleEarned.innerHTML = usrBetPossible;
};
function updateUsrBank(){
    if(spinnedVal.every( (val, i, arr) => val === arr[0] )){
        usrBankVariable = (usrBankVariable) + (usrBetPossible);
        usrBetVariable = 0;
        usrBetPossible = 0;
        updateBankBet();
        updateBankPossibleEarned();
    };
    userBank.innerHTML = usrBankVariable;
};
function controlAction(){
    updateUsrBank();
    updateBankPossibleEarned();
    updateBankBet();
};


//===: Listeners :===
btnSpin.addEventListener('click', function onClick(e){
    if(usrBankVariable > 0){
        btnSpin.classList.add("anmSpinner");
        spinSlots();
        updateBankBet();
        usrBankVariable = usrBankVariable - usrBetVariable;
        updateUsrBank();
        for(let i=0; i<(arrMultiplies.length-1); i++){
            handleSpinAnimation(i);
        };
        console.log("SALDO:", usrBankVariable)
    }else{
        console.log("SALDO INSUFICIENTE");
    }
});
btnControlIncrease.addEventListener('click', function onCLick(e) {
    usrBetVariable = usrBetVariable + 5;
    controlAction();
});
btnControlDecrease.addEventListener('click', function onCLick(e) {
    if(usrBetVariable > 0){
        usrBetVariable = usrBetVariable - 5;
        controlAction();
    };
});

document.addEventListener('DOMContentLoaded', () => {
    // Obtener elementos del DOM
    const btnSpin = document.getElementById('btnSpin');
    const rouletteMainLeft = document.getElementById('rouletteMainLeft');
    const rouletteMainMiddle = document.getElementById('rouletteMainMiddle');
    const rouletteMainRight = document.getElementById('rouletteMainRight');
  
    // Función para generar un número aleatorio entre 1 y 4
    function getRandomNumber() {
      return Math.floor(Math.random() * 4) + 1;
    }
  
    // Función para rotar los carretes
    function rotateReels() {
      // Generar números aleatorios para cada carrete
      const randomNumberLeft = getRandomNumber();
      const randomNumberMiddle = getRandomNumber();
      const randomNumberRight = getRandomNumber();
  
      // Deshabilitar el botón de inicio durante el giro
      btnSpin.disabled = true;
  
      // Simular el giro de los carretes durante 5 segundos
      setTimeout(() => {
        // Mostrar los resultados finales en los carretes
        rouletteMainLeft.innerHTML = `
          <div class="slotsResults">
            <img src="static/img/slotsGame/logo${randomNumberLeft}.jpeg" alt="">
          </div>
        `;
  
        rouletteMainMiddle.innerHTML = `
          <div class="slotsResults">
            <img src="static/img/slotsGame/logo${randomNumberMiddle}.jpeg" alt="">
          </div>
        `;
  
        rouletteMainRight.innerHTML = `
          <div class="slotsResults">
            <img src="static/img/slotsGame/logo${randomNumberRight}.jpeg" alt="">
          </div>
        `;
  
        // Habilitar el botón de inicio nuevamente
        btnSpin.disabled = false;
      }, 5000);
    }
  
    // Agregar evento de clic al botón de inicio
    btnSpin.addEventListener('click', rotateReels);
  });
  

//===: EXECUTION :===
updateUsrBank();
controlAction();