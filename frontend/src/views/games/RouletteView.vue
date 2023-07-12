<template>
    <div class="p-6 bg-green-800 text-white rounded-lg">
        <h1 class="text-3xl font-bold mb-4">Roulette</h1>
        <div class="mb-4 flex space-x-2">
            <img v-for="token in tokens" :key="token"
                :src="`http://127.0.0.1:5004/api/static/games/rouletteGame/token${token}.png`"
                :class="['p-2', 'rounded', 'w-20',selectedToken === token ? 'ring-2 ring-yellow-500' : '']"
                @click="selectedToken = token"
                alt="token"
                width="50"
                height="50">
        </div>
        <div class="grid grid-cols-12">
            <div v-for="col in 12" :key="col" class="flex flex-col">
                <div class="flex items-center justify-center border-2 border-white">
                    <button
                        :class="['p-2', 'w-full', 'h-full', 'rounded', 'p-5', isSelected(col * 3) ? 'bg-yellow-500 text-black' : (col * 3) % 2 !== 0 ? 'bg-red-500' : 'bg-black']"
                        @click="placeBet(col * 3)">
                        {{ col * 3 }}
                    </button>
                </div>
                <div class="flex items-center justify-center border-2 border-white ">
                    <button
                        :class="['p-2', 'w-full', 'h-full', 'rounded', 'p-5', isSelected(col * 3 - 1) ? 'bg-yellow-500 text-black' : (col * 3 - 1) % 2 !== 0 ? 'bg-red-500' : 'bg-black']"
                        @click="placeBet(col * 3 - 1)">
                        {{ col * 3 - 1 }}
                    </button>
                </div>
                <div class="flex items-center justify-center border-2 border-white ">
                    <button
                        :class="['p-2', 'w-full', 'h-full', 'rounded', 'p-5', isSelected(col * 3 - 2) ? 'bg-yellow-500 text-black' : (col * 3 - 2) % 2 !== 0 ? 'bg-red-500' : 'bg-black']"
                        @click="placeBet(col * 3 - 2)">
                        {{ col * 3 - 2 }}
                    </button>
                </div>
            </div>
        </div>
        <button class="mt-4 p-2 bg-green-500 text-white rounded" @click="submitBet">Submit Bet</button>
        <!-- TODO: Add the buttons for the other bet types -->
        <div v-if="result" class="text-yellow-500">{{ result }}</div>
        <div v-else class="text-gray-500">Esperando resultado...</div>
    </div>
</template>
  
<script>
import axios from 'axios'

export default {
    data() {
        return {
            selectedToken: null,
            tokens: [5, 10, 25],
            result: null,
            betting: false,
            selectedNumbers: []
        }
    },
    methods: {
        placeBet(number) {
            if (!this.selectedToken) {
                alert('Please select a token before placing a bet.')
                return
            }
            if (this.isSelected(number)) {
                this.selectedNumbers = this.selectedNumbers.filter(bet => bet.value !== number)
            } else {
                this.selectedNumbers.push({ type: 'number', value: number, amount: this.selectedToken })
            }
        },
        isSelected(number) {
            return this.selectedNumbers.some(bet => bet.value === number)
        },
        async submitBet() {
            if (this.selectedNumbers.length === 0) {
                alert('Please place at least one bet.')
                return
            }
            this.betting = true
            const response = await axios.post('/roulette/bet', { bet_data: this.selectedNumbers })
            if (response.status === 201) {
                const betId = response.data.id;
                const resultResponse = await axios.get(`roulette/result?bet_id=${betId}`);
                if (resultResponse.status === 200) {
                    
                    const resultData = resultResponse.data;
                    console.log(resultData)
                    // si es red guardar como rojo y si es black como negro
                    const winningNumber = resultData.numbers;
                    const winningColor = (resultData.color == 'red') ? 'rojo' : 'negro';

                    let winAmount = 0;
                    let loseAmount = 0;
                    let win = false;
                    let results = response.data.bet_data;

                    // pasar results a json
                    results = JSON.parse(results)
                    
                    console.log(results)

                    results.forEach(bet => {
                        if (bet.result === 'win') {
                            winAmount += bet.amount;
                            win = true;
                        } else {
                            loseAmount += bet.amount;
                        }
                    });
                    this.result = win ? `¡Ganaste ${winAmount}! El número ganador es ${winningNumber} - ${winningColor}` : `Perdiste ${loseAmount}. El número ganador es ${winningNumber} ${winningColor}`;

                } else {
                    this.result = 'Error';
                }
            } else {
                this.result = 'Error';
            }
            this.betting = false
            this.selectedNumbers = []
        }
    }
}
</script>