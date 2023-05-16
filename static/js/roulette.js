//===: General
console.log("===: TumiPalace | Roulette Logic :===");


//===: Variables
// Elementos HTML
const tokens = document.querySelectorAll('.tokenCoin');
const tokenNumbers = document.querySelectorAll('.token');
let actionSelected = document.getElementById("actionSelected");
let btnActionSelected = document.getElementById("btnActionSelected");
let rouletteCounterSec = document.getElementById("rouletteCounterSec");
let rouletteCounter = document.getElementById("rouletteCounter");
let rouletteSpin = document.getElementById("rouletteSpin");
let pasedSelected = document.getElementById("playedActions1");
let salaryCounter = document.getElementById("userSalary");
let winnerValueCont = document.getElementById("winnerVal");
let winnerWrapper = document.getElementById("winnerWrapper");

// Valores y arreglos
const arrTokens = [['1'], ['5'], ['10'], ['25'], ['50'], ['100']];
const arrTweaks = [['34', '1st 12'], ['35', '2nd 12'], ['36', '3rd 12'], ['37', '1 to 18'], ['38', '19 to 36'], ['39', 'Even'], ['40', 'Odd']];
let tempSelected = ['0', '0'];
let currentToken, idx;
let usrSalary = 1940.50;
const szTokens = 6;
let winnerValue = 0;

//===: Functions
calcBank();

// Calcula las acciones jugadas

function calcPlayed(){
    arrTokens.forEach(arrToken => {
        console.log(arrToken);
    });
};

// Calcula el saldo del usuario

function calcBank(){
    getSalary(); // Obtiene el salario inicial.
};

// Obtiene el salario del usuario

function getSalary(){
    salaryCounter.innerHTML = usrSalary;
};

// Boton de Spin

let isClicked = false;
rouletteSpin.addEventListener('click', function onclick(event){
    const randomNumber = Math.floor(Math.random() * 34); // Generar número aleatorio entre 0 y 99
    console.log("Número aleatorio:", randomNumber);
});


//Selecciona el numero
for(let i=0; i<tokenNumbers.length; i++){
    tokenNumbers[i].addEventListener('click', function onclick(e){
        console.log(tokenNumbers[i].textContent);
        tempSelected[1] = tokenNumbers[i].textContent;
        actionSelected.innerHTML = `${tempSelected[0]}, ${tempSelected[1]}`;
    });
};

//Evento de clic en los tokens

for(const token of tokens){
    token.disabled = true;
    token.addEventListener('click', function onclick(e) {
        e.preventDefault();
        
        currentToken = ((token.id).substring(5)).toString();
        tempSelected[0] = currentToken;
        actionSelected.innerHTML = `${tempSelected[0]}, ${tempSelected[1]}`;
        const pos = arrTokens.findIndex((subArr) => subArr[0] == currentToken); // return pos[0] of selected item
    });
};

// Evento de clic en el botón de acción seleccionada
btnActionSelected.addEventListener('click', function onclick(e) {
    console.log("CLICKED", tempSelected[0]);
    if(tempSelected[0] == "0"){
        btnActionSelected.disabled = true;
    }else{
        btnActionSelected.disabled = false;
    }
    const pos = arrTokens.findIndex((subArr) => subArr[0] == tempSelected[0]);
    if(tempSelected[1].length > 2){
        const fixToNum = arrTweaks.findIndex((subArr) => subArr[1] == tempSelected[1]);
        console.log(fixToNum);
        tempSelected[1] = arrTweaks[fixToNum][0];
    }
    console.log(arrTokens);
    arrTokens[pos].push(tempSelected[1]);
    let nameSelect = `playedActions${tempSelected[0]}`;
    let tokenSelected = document.getElementById(nameSelect);
    tokenSelected.innerHTML = (arrTokens[pos]).slice(1).join(' - ');
    
    tempSelected[0] = '0';
    tempSelected[1] = '0';
    actionSelected.innerHTML = `${tempSelected[0]}, ${tempSelected[1]}`;
});
