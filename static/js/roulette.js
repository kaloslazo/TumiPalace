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
const arrTweaks = [[ 1, 12, '1st 12'], [  13,  24, '2nd 12'], [25 , 36 , '3rd 12'], [1 , 18, '1 to 18'], [19 , 36, '19 to 36'], [ 1,  36, 'Even'], [ 1 , 36, 'Odd']];
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
calcBank();

function calcPlayed(){
    arrTokens.forEach(arrToken => {
        console.log(arrToken);
    });
};

function calcBank(){
    getSalary(); 
};

function getSalary(){
    salaryCounter.innerHTML = usrSalary;
};

// Boton de Spin

let isClicked = false;
rouletteSpin.addEventListener('click', function onclick(event){
    getSalary()

    const randomNumber = Math.floor(Math.random() * 34); // Generar número aleatorio entre 0 y 99
    console.log(values_numero)
    console.log(arrTokens)
    temp = 0
    if(values_numero.includes(randomNumber)){
        for ( let i  = 0 ; i < arrTokens.length ; i++){
            if(arrTokens[i].includes(randomNumber)){
                suma = arrTokens[i][0] * 2
                console.log("suma", suma)
                temp += suma
            }else{
               console.log("NO SALE")       
            }
        }
    }
    usrSalary += temp
    console.log("usrSalary" , usrSalary     )
    getSalary()
    arrTokens = [[ 1], [5], [10], [25], [50], [100]];
    values_numero = []
    for(let i = 0 ; i < arrTokens.length; i ++){
        let nameSelect = `playedActions${arrTokens[i][0]}`;
        let tokenSelected = document.getElementById(nameSelect);
        tokenSelected.innerHTML = "";
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
        const fixToNum = arrTweaks.findIndex((subArr) => subArr[2] == tempSelected[1]);
        console.log("fixToNum", fixToNum);
        tempSelected[1] = arrTweaks[fixToNum][2];
        console.log( "TEMP ", arrTweaks[fixToNum][1])
        for(let i = arrTweaks[fixToNum][0]; i <= arrTweaks[fixToNum][1] ; i ++){
            arrTokens[pos].push(parseInt(i))
            values_numero.push(parseInt(i))
        }
        console.log(  "ARR : ", arrTokens)
    }else{
        console.log(" Arr" , arrTokens);
        arrTokens[pos].push(parseInt(tempSelected[1]));
        values_numero.push(parseInt(tempSelected[1]))
    }
    let nameSelect = `playedActions${tempSelected[0]}`;
    let tokenSelected = document.getElementById(nameSelect);

    tokenSelected.innerHTML = (arrTokens[pos]).slice(1).join(' - ');
    console.log(values_numero)
    tempSelected[0] = '0';
    tempSelected[1] = '0';
    actionSelected.innerHTML = `${tempSelected[0]}, ${tempSelected[1]}`;
    
});

// Obtener referencia al botón Clear
const clearButton = document.getElementById('rouletteClear');

// Agregar evento de clic al botón Clear
clearButton.addEventListener('click', resetTokens);

// Función para reiniciar los tokens
function resetTokens() {
    arrTokens = [[1], [5], [10], [25], [50], [100]];
    values_numero = [];
    
    for (let i = 0; i < arrTokens.length; i++) {
      let nameSelect = `playedActions${arrTokens[i][0]}`;
      let tokenSelected = document.getElementById(nameSelect);
      tokenSelected.innerHTML = "-";
    }
  }
