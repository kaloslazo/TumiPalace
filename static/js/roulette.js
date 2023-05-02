//===: General
console.log("===: TumiPalace | Roulette Logic :===");


//===: Variables
const tokens = document.querySelectorAll('.tokenCoin');
const tokenNumbers = document.querySelectorAll('.token');
const arrTokens = [['1'], ['5'], ['10'], ['25'], ['50'], ['100']];
const arrTweaks = [['34', '1st 12'], ['35', '2nd 12'], ['36', '3rd 12'], ['37', '1 to 18'], ['38', '19 to 36'], ['39', 'Even'], ['40', 'Odd']];

let actionSelected = document.getElementById("actionSelected");
let btnActionSelected = document.getElementById("btnActionSelected");
let rouletteCounterSec = document.getElementById("rouletteCounterSec");
let rouletteCounter = document.getElementById("rouletteCounter");
let rouletteSpin = document.getElementById("rouletteSpin");

let tempSelected = ['0', '0'];
let currentToken, idx;
actionSelected.innerHTML = `0, 0`;
let pasedSelected = document.getElementById("playedActions1");

let salaryCounter = document.getElementById("userSalary");
let usrSalary = 1940.50;
const szTokens = 6;

let winnerValueCont = document.getElementById("winnerVal");
let winnerWrapper = document.getElementById("winnerWrapper");

let winnerValue = 0;

//===: Functions
calcBank();

function calcPlayed(){
    arrTokens.forEach(arrToken => {
        console.log(arrToken);
    });
};

function calcBank(){
    getSalary(); // first fetch to salary.
};

function getRandomValue(){
    const randomVal = Math.random();
    winnerValue = Math.floor(randomVal * 36); // multiply for possibles values.
    salaryCounter.innerHTML = usrSalary - winnerValue;
    winnerWrapper.style.visibility = "visible";
    winnerValueCont.innerHTML = winnerValue;
};
function getSalary(){
    salaryCounter.innerHTML = usrSalary;
};

const counterLimit = 5;
let timeRemaining = counterLimit;
let timeRepeat = 5;
let isClicked = false;
rouletteSpin.addEventListener('click', function onclick(event){
    event.preventDefault();
    isClicked = true;
    if(isClicked){
        const timer = setInterval(() => {
            rouletteSpin.disabled = true;
            timeRemaining--;
            if(timeRemaining <= 0){
                console.log("Tiempo terminado.");
                calcBank();
                calcPlayed();
                clearInterval(timer);
            }else {
                rouletteCounterSec.innerHTML = timeRemaining;
            };
        }, 1000);
    };
    isClicked = false;
});


//===: Events
for(let i=0; i<tokenNumbers.length; i++){
    tokenNumbers[i].addEventListener('click', function onclick(e){
        console.log(tokenNumbers[i].textContent);
        tempSelected[1] = tokenNumbers[i].textContent;
        actionSelected.innerHTML = `${tempSelected[0]}, ${tempSelected[1]}`;
    });
};

for(const token of tokens){
    token.disabled = true;
    token.addEventListener('click', function onclick(e) {
        e.preventDefault();
        
        currentToken = ((token.id).substring(5)).toString();
        tempSelected[0] = currentToken;
        actionSelected.innerHTML = `${tempSelected[0]}, ${tempSelected[1]}`;
        // const pos = arrTokens.findIndex((subArr) => subArr[0] == currentToken); // return pos[0] of selected item
    });
};

btnActionSelected.addEventListener('click', function onclick(e) {
    console.log("CLICKED", tempSelected[0]);
    if(tempSelected[0] == "0"){
        btnActionSelected.disabled = true;
    }else{
        btnActionSelected.disabled = false;
    };
    const pos = arrTokens.findIndex((subArr) => subArr[0] == tempSelected[0]);
    if(tempSelected[1].length > 2){
        const fixToNum = arrTweaks.findIndex((subArr) => subArr[1] == tempSelected[1]);
        console.log(fixToNum);
        tempSelected[1] = arrTweaks[fixToNum][0];
    };
    console.log(arrTokens);
    arrTokens[pos].push(tempSelected[1]);
    let nameSelect = `playedActions${tempSelected[0]}`;
    let tokenSelected = document.getElementById(nameSelect);
    tokenSelected.innerHTML = (arrTokens[pos]).slice(1).join(' - ');
    tempSelected[0] = '0';
    tempSelected[1] = '0';
    actionSelected.innerHTML = `${tempSelected[0]}, ${tempSelected[1]}`;
});