<template>
    <div class="p-6  text-white rounded-lg">
        <h2 class="text-white border-b-2 border-yellow-600 py-2 mb-10 font-semibold text-2xl">Ruleta del Inca</h2>

        <div class="background_roulette px-16 py-10  z-0">
            <div class="relative">
                <div class="grid grid-cols-12  z-50">
                    <div v-for="col in 12" :key="col" class="flex flex-col">
                        <div class="flex items-center justify-center border-2 border-white">
                            <button
                                :class="['p-2', 'w-full', 'h-full', 'rounded', 'p-5', isSelected(col * 3) ? 'bg-yellow-700 text-black' : (col * 3) % 2 !== 0 ? 'bg-red-500' : 'bg-black']"
                                @click="placeBet(col * 3)">
                                {{ col * 3 }}
                            </button>
                        </div>
                        <div class="flex items-center justify-center border-2 border-white ">
                            <button
                                :class="['p-2', 'w-full', 'h-full', 'rounded', 'p-5', isSelected(col * 3 - 1) ? 'bg-yellow-700 text-black' : (col * 3 - 1) % 2 !== 0 ? 'bg-red-500' : 'bg-black']"
                                @click="placeBet(col * 3 - 1)">
                                {{ col * 3 - 1 }}
                            </button>
                        </div>
                        <div class="flex items-center justify-center border-2 border-white ">
                            <button
                                :class="['p-2', 'w-full', 'h-full', 'rounded', 'p-5', isSelected(col * 3 - 2) ? 'bg-yellow-700 text-black' : (col * 3 - 2) % 2 !== 0 ? 'bg-red-500' : 'bg-black']"
                                @click="placeBet(col * 3 - 2)">
                                {{ col * 3 - 2 }}
                            </button>
                        </div>
                    </div>
                </div>
    
                <div class="mt-10 flex space-x-2">
                    <img v-for="token in tokens" :key="token"
                        :src="`http://127.0.0.1:5004/api/static/games/rouletteGame/token${token}.png`"
                        :class="['p-2', 'rounded', 'w-20',selectedToken === token ? 'ring-2 ring-yellow-500' : '']"
                        @click="selectedToken = token"
                        alt="token"
                        width="50"
                        height="50">
                </div>
    
                <button class="bg-yellow-700 text-black px-10 py-3 font-medium mt-10 rounded" @click="submitBet">Apostar</button>
                <!-- TODO: Add the buttons for the other bet types -->
                <div v-if="result" class="text-yellow-500">{{ result }}</div>
            </div>
        </div>
    </div>
</template>

<style>
.background_roulette {
    position: relative;
    background-color: #382c27;
    background-image: url('http://127.0.0.1:5004/api/static/games/rouletteGame/casino-roulette-felt.jpg');
    background-repeat: no-repeat;
    background-size: cover;
}

.background_roulette::before {
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background-color: #382c270d;
    box-shadow: inset 10px 50px 100px rgba(0, 0, 0, 0.2),
                inset -10px 50px 100px rgba(0, 0, 0, 0.2),
                inset 10px -50px 100px rgba(0, 0, 0, 0.2),
                inset -10px -50px 100px rgba(0, 0, 0, 0.2);
}
</style>
  
<script>
import axios from 'axios'

export default {
    data() {
        return {
            selectedToken: null,
            tokens: [5, 10, 25, 50, 100],
            result: null,
            betting: false,
            selectedNumbers: []
        }
    },
    computed: {
        user_data() { return this.$store.getters.user_data },
        balance() { return this.$store.getters.user_data.bank },
    },
    methods: {
        placeBet(number) {
            if (!this.selectedToken) {
                alert('Debes seleccionar un token para apostar.')
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
                alert('Debes seleccionar un número para apostar.')
                return
            }
            this.betting = true
            const response = await axios.post('/roulette/bet', { bet_data: this.selectedNumbers })
            try {
                const betId = response.data.id;
                const resultResponse = await axios.get(`roulette/result?bet_id=${betId}`);
                
                try {
                    
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

                } catch(err) { this.result = err.response.data.message; }

            } catch(err) {
                this.result = err.response.data.message;
            }
            this.betting = false
            this.selectedNumbers = []
        },
        async updateBalance(newBalance) {
            try {
                const response = await axios.post(`/users/${this.$store.getters.user_data.id}/update_balance`, { balance: newBalance });
                this.$store.commit('updateUserBank', newBalance);
            } catch (err) {
                this.error = err.response.data.message;
                this.$refs.noBalanceSound.play();
            }
        }
    }
}
</script>