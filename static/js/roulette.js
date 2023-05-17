//===: General
console.log("===: TumiPalace | Roulette Logic :===");


//===: Variables
// Elementos HTML

const tokens = document.querySelectorAll('.tokenCoin');
const TOKENS = document.getElementsByClassName('tokenCoin')
const tokensID = document.getElementById("rouletteMenu")
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
var arrTokens = [[ 1], [5], [10], [25], [50], [100]];
var values_numero = []
const values = [[ "token1" ,1], [ "token5" ,5 ], ["token10", 10], ["token25" , 25], [ "token50" , 50 ], [ "token100" , 100 ]];
const arrTweaks = [['34', '1st 12'], ['35', '2nd 12'], ['36', '3rd 12'], ['37', '1 to 18'], ['38', '19 to 36'], ['39', 'Even'], ['40', 'Odd']];
const arr1=[]
const arr5=[]
const arr10=[]
const arr25=[]
const arr50=[]
const arr100=[]
let tempSelected = ['0', '0'];
let currentToken, idx;
let usrSalary = 1940.0;
const szTokens = 6;
let winnerValue = 0;

//===: Functions
function calcBank() {
}

// Calcula las acciones jugadas

function calcPlayed(){
    arrTokens.forEach(arrToken => {
        console.log(arrToken);
    });
};

// Obtiene el salario del usuario

function getSalary(){
    salaryCounter.innerHTML = usrSalary;
};

// Boton de Spin

let isClicked = false;
rouletteSpin.addEventListener('click', function onclick(event) {
    getSalary();

    if (usrSalary <= 0){
        document.getElementById("resultadoAviso").innerHTML = "¡Saldo insuficiente!";
        return;
    }
    const randomNumber = Math.floor(Math.random() * 34); // Generar número aleatorio entre 0 y 99
    console.log(values_numero);
    console.log(arrTokens);
    temp = 0;
    if (values_numero.includes(randomNumber)) {
        for (let i = 0; i < arrTokens.length; i++) {
            if (arrTokens[i].includes(randomNumber)) {
                temp += arrTokens[i][0] * 2;
            }
        }
    }
    usrSalary += temp;
    getSalary();

    if (temp === 0) {
        document.getElementById("resultadoAviso").innerHTML = "¡Perdiste!";
    } else {
        document.getElementById("resultadoAviso").innerHTML = "¡Ganaste!";
    }

    console.log("Número aleatorio:", randomNumber);
});

for(let i = 0 ; i < TOKENS.length ; i ++){
    TOKENS[i].addEventListener("click", function(){
        const ButonID = values[i][1];
        usrSalary -= ButonID 
    })
}


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
    arrTokens[pos].push(parseInt(tempSelected[1]));
    let nameSelect = `playedActions${tempSelected[0]}`;
    let tokenSelected = document.getElementById(nameSelect);
    tokenSelected.innerHTML = (arrTokens[pos]).slice(1).join(' - ');
    values_numero.push(parseInt(tempSelected[1]))
    console.log(values_numero)
    tempSelected[0] = '0';
    tempSelected[1] = '0';
    actionSelected.innerHTML = `${tempSelected[0]}, ${tempSelected[1]}`;
});
