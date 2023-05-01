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

let tempSelected = ['0', '0'];
let currentToken, idx;
actionSelected.innerHTML = `0, 0`;

let salaryCounter = document.getElementById("userSalary");
let usrSalary = 1940.50;

//===: Functions
getSalary(); // first fetch to salary.
function getRandomValue(){
    const randomVal = Math.random();
    const nVal = Math.floor(randomVal * 36); // multiply for possibles values.
    salaryCounter.innerHTML = nVal;
};
function getSalary(){
    salaryCounter.innerHTML = usrSalary;
};

const counterLimit = 11;
let timeRemaining = counterLimit;
const timer = setInterval(() => {
    timeRemaining--;
    if(timeRemaining <= 0){
        console.log("Tiempo terminado.");
        // for(let i=0; i<tokenNumbers.length; i++){
        //     tokenNumbers[i].disabled = true;
        // }; 
        // for(const token of tokens){
        //     token.disabled = true;
        // };
        // clearInterval(timer);
    }else {
        rouletteCounterSec.innerHTML = timeRemaining;
    };
}, 1000);


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
    arrTokens[pos].push(tempSelected[1]);
    tempSelected[0] = '0';
    tempSelected[1] = '0';
    actionSelected.innerHTML = `${tempSelected[0]}, ${tempSelected[1]}`;
    console.log(arrTokens);
});