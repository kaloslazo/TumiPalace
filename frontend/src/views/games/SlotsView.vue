<template>
    <div class="px-6">
        <h2 class="text-white border-b-2 border-yellow-600 py-2 mb-10 font-semibold text-2xl">Fortuna del Sol</h2>

        <div class="background_slot shadow-2xl">
            <div class="absolute inset-0 bg-black opacity-50"></div>

            <div class="relative">
                <!-- contenedor tragamonedas -->
                <div class="flex flex-col justify-center items-center gap-4 mx-auto py-10 z-50">
                    <!-- iterar elementos -->
                    <div class="border_image bg-brown-1000">
                        <div class="flex justify-center items-center">
                            <div v-for="(col, colIndex) in matrix[0].length" :key="colIndex" class="column"
                                :class="{ 'border-image-right': colIndex < matrix[0].length - 1 }">
                                <div v-for="(row, rowIndex) in matrix" :key="rowIndex"
                                    class="text-6xl py-4 pl-4 pr-4 bg-brown-950 border-2 border-brown-1000 shadow-inner">
                                    <div class="border-4 border-brown-1000 rounded-lg p-2 bg-brown-1000 shadow-inner">
                                        <img :src="matrix[rowIndex][colIndex].imageUrl" alt="imagen de juego"
                                            class="mx-auto w-16" />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- iterar elementos-->
                </div>
                <!-- contenedor tragamonedas -->
                <div class="flex items-center justify-center py-5 gap-10">
                    <div class="flex items-center justify-center gap-2 flex-col text-center text-white">
                        <label class="font-medium text-base" for="bet">Apuesta</label>
                        <input class="bg-yellow-600 rounded-sm px-2 py-1 text-black font-medium text-center" id="bet"
                            v-model.number="bet" type="number" min="1" :max="balance" />
                    </div>
                    <button id="btn_spin" @click="spin" :disabled=isSpinning
                        class="flex flex-col items-center justify-center">
                        <img class="w-28 shadow-" src="http://127.0.0.1:5004/api/static/games/slotsGame/actionStart.png"
                            alt="">
                    </button>
                    <div class="flex items-center justify-center gap-2 flex-col text-center text-white">
                        <span class="font-medium text-base" for="bet">Saldo</span>
                        <p class="bg-yellow-600 rounded-sm px-4 py-1 text-black font-medium">{{ balance }}</p>
                    </div>
                </div>

                <div class="absolute bottom-0 right-0 mb-4 mr-4">
                    <ShowSuccess :success="result" :title="title_bet"/>
                    <ShowError :error="error"/>
                </div>
            </div>
        </div>
    </div>

    <audio ref="spinSound" :src="baseURL + '/api/static/games/slotsGame/push_bet.mp3'"></audio>
    <audio ref="winSound" :src="baseURL + '/api/static/games/slotsGame/bet_winner.mp3'"></audio>
    <audio ref="betLoadingSound" :src="baseURL + '/api/static/games/slotsGame/bet_loading.mp3'"></audio>
    <audio ref="noBalanceSound" :src="baseURL + '/api/static/games/slotsGame/error_bet.mp3'"></audio>
</template>

<style>
#btn_spin:disabled {
    cursor: not-allowed;
    opacity: 0.8;
}

.spin {
    transition: opacity 0.3s;
}

.border_image {
    border-width: 1em;
    border-style: solid;
    border-image: url('http://127.0.0.1:5004/api/static/games/slotsGame/borderSlots.jpg') 30 30 round;
}

.column {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.border-image-right {
    border-right: 1em solid transparent;
    border-image: url('http://127.0.0.1:5004/api/static/games/slotsGame/borderSlots.jpg') 30 30 round;
}

.background_slot {
    position: relative;
    background-color: #382c27;
    background-image: url('http://127.0.0.1:5004/api/static/games/slotsGame/wallpaper-macchu.png');
    background-repeat: no-repeat;
    background-size: cover;
}

.background_slot::before {
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background-color: #382c270d;
}

.background_slot_2 {
    background-color: #382c27;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='88' height='88' viewBox='0 0 88 88'%3E%3Cg fill='%23fbbf24' fill-opacity='0.05'%3E%3Cpath fill-rule='evenodd' d='M29.42 29.41c.36-.36.58-.85.58-1.4V0h-4v26H0v4h28c.55 0 1.05-.22 1.41-.58h.01zm0 29.18c.36.36.58.86.58 1.4V88h-4V62H0v-4h28c.56 0 1.05.22 1.41.58zm29.16 0c-.36.36-.58.85-.58 1.4V88h4V62h26v-4H60c-.55 0-1.05.22-1.41.58h-.01zM62 26V0h-4v28c0 .55.22 1.05.58 1.41.37.37.86.59 1.41.59H88v-4H62zM18 36c0-1.1.9-2 2-2h10a2 2 0 1 1 0 4H20a2 2 0 0 1-2-2zm0 16c0-1.1.9-2 2-2h10a2 2 0 1 1 0 4H20a2 2 0 0 1-2-2zm16-26a2 2 0 0 1 2-2 2 2 0 0 1 2 2v4a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-4zm16 0a2 2 0 0 1 2-2 2 2 0 0 1 2 2v4a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-4zM34 58a2 2 0 0 1 2-2 2 2 0 0 1 2 2v4a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-4zm16 0a2 2 0 0 1 2-2 2 2 0 0 1 2 2v4a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-4zM34 78a2 2 0 0 1 2-2 2 2 0 0 1 2 2v6a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-6zm16 0a2 2 0 0 1 2-2 2 2 0 0 1 2 2v6a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-6zM34 4a2 2 0 0 1 2-2 2 2 0 0 1 2 2v6a2 2 0 0 1-2 2 2 2 0 0 1-2-2V4zm16 0a2 2 0 0 1 2-2 2 2 0 0 1 2 2v6a2 2 0 0 1-2 2 2 2 0 0 1-2-2V4zm-8 82a2 2 0 1 1 4 0v2h-4v-2zm0-68a2 2 0 1 1 4 0v10a2 2 0 1 1-4 0V18zM66 4a2 2 0 1 1 4 0v8a2 2 0 1 1-4 0V4zm0 72a2 2 0 1 1 4 0v8a2 2 0 1 1-4 0v-8zm-48 0a2 2 0 1 1 4 0v8a2 2 0 1 1-4 0v-8zm0-72a2 2 0 1 1 4 0v8a2 2 0 1 1-4 0V4zm24-4h4v2a2 2 0 1 1-4 0V0zm0 60a2 2 0 1 1 4 0v10a2 2 0 1 1-4 0V60zm14-24c0-1.1.9-2 2-2h10a2 2 0 1 1 0 4H58a2 2 0 0 1-2-2zm0 16c0-1.1.9-2 2-2h10a2 2 0 1 1 0 4H58a2 2 0 0 1-2-2zm-28-6a2 2 0 1 0 0-4 2 2 0 0 0 0 4zm8 26a2 2 0 1 0 0-4 2 2 0 0 0 0 4zm16 0a2 2 0 1 0 0-4 2 2 0 0 0 0 4zM36 20a2 2 0 1 0 0-4 2 2 0 0 0 0 4zm16 0a2 2 0 1 0 0-4 2 2 0 0 0 0 4zm-8-8a2 2 0 1 0 0-4 2 2 0 0 0 0 4zm0 68a2 2 0 1 0 0-4 2 2 0 0 0 0 4zm16-34a2 2 0 1 0 0-4 2 2 0 0 0 0 4zm16-12a2 2 0 1 0 0 4 6 6 0 1 1 0 12 2 2 0 1 0 0 4 10 10 0 1 0 0-20zm-64 0a2 2 0 1 1 0 4 6 6 0 1 0 0 12 2 2 0 1 1 0 4 10 10 0 1 1 0-20zm56-12a2 2 0 1 0 0-4 2 2 0 0 0 0 4zm0 48a2 2 0 1 0 0-4 2 2 0 0 0 0 4zm-48 0a2 2 0 1 0 0-4 2 2 0 0 0 0 4zm0-48a2 2 0 1 0 0-4 2 2 0 0 0 0 4zm24 32a10 10 0 1 1 0-20 10 10 0 0 1 0 20zm0-4a6 6 0 1 0 0-12 6 6 0 0 0 0 12zm36-36a6 6 0 1 1 0-12 6 6 0 0 1 0 12zm0-4a2 2 0 1 0 0-4 2 2 0 0 0 0 4zM10 44c0-1.1.9-2 2-2h8a2 2 0 1 1 0 4h-8a2 2 0 0 1-2-2zm56 0c0-1.1.9-2 2-2h8a2 2 0 1 1 0 4h-8a2 2 0 0 1-2-2zm8 24c0-1.1.9-2 2-2h8a2 2 0 1 1 0 4h-8a2 2 0 0 1-2-2zM3 68c0-1.1.9-2 2-2h8a2 2 0 1 1 0 4H5a2 2 0 0 1-2-2zm0-48c0-1.1.9-2 2-2h8a2 2 0 1 1 0 4H5a2 2 0 0 1-2-2zm71 0c0-1.1.9-2 2-2h8a2 2 0 1 1 0 4h-8a2 2 0 0 1-2-2zm6 66a6 6 0 1 1 0-12 6 6 0 0 1 0 12zm0-4a2 2 0 1 0 0-4 2 2 0 0 0 0 4zM8 86a6 6 0 1 1 0-12 6 6 0 0 1 0 12zm0-4a2 2 0 1 0 0-4 2 2 0 0 0 0 4zm0-68A6 6 0 1 1 8 2a6 6 0 0 1 0 12zm0-4a2 2 0 1 0 0-4 2 2 0 0 0 0 4zm36 36a2 2 0 1 0 0-4 2 2 0 0 0 0 4z'/%3E%3C/g%3E%3C/svg%3E");
}
</style>

<script>
import ShowError from '@/components/ShowError.vue';
import ShowSuccess from '@/components/ShowSuccess.vue';
import axios from 'axios';

export default {
    data() {
        return {
            baseURL: "http://127.0.0.1:5004",
            symbols: [
                { name: 'logo1', imageUrl: 'http://127.0.0.1:5004/api/static/games/slotsGame/logo1.png', multiplier: 10 },
                { name: 'logo2', imageUrl: 'http://127.0.0.1:5004/api/static/games/slotsGame/logo2.png', multiplier: 8 },
                { name: 'logo3', imageUrl: 'http://127.0.0.1:5004/api/static/games/slotsGame/logo3.png', multiplier: 5 },
                { name: 'logo4', imageUrl: 'http://127.0.0.1:5004/api/static/games/slotsGame/logo4.png', multiplier: 2 },
            ],
            matrix: Array(4).fill().map(() => Array(4).fill(null)),
            bet: 1,
            isSpinning: false,
            title_bet: "No te desanimes",
            result: '',
            error: '',
        }
    },
    created() {
        // que la matriz sea aleatorio
        this.matrix = this.matrix.map(row => row.map(() => this.getRandomSymbol()));
    },
    computed: {
        user_data() { return this.$store.getters.user_data },
        balance() { return this.$store.getters.user_data.bank },
    },
    components: {
        ShowError,
        ShowSuccess
    },
    methods: {
        async spin() {
            this.result = "";
            this.error = "";
            this.title_bet = "No te desanimes";

            // todos los signos iguales -> x5
            // dos signos iguales -> x2
            // todos los signos distintos -> pierde la apuesta 

            // -> verificar apuesta
            if (this.bet < 1) {
                this.error = "La apuesta debe ser mayor a 1.";
                this.$refs.noBalanceSound.play();
                return; 
            }
            if (this.bet > this.balance) { 
                this.error = 'No tienes suficiente saldo para esta apuesta.';
                this.$refs.noBalanceSound.play();
                return; 
            }


            // -> inicia logica de giro
            this.$refs.spinSound.play();
            this.$store.commit('updateUserBank', this.balance - this.bet);
            try {
                const response = await axios.post(`/users/${this.$store.getters.user_data.id}/update_balance`, { balance: this.balance });
                this.$store.commit('updateUserBank', this.balance);
                console.log(response.data.message);
            } catch (err) {
                this.$refs.noBalanceSound.play();
                this.error = err.response.data.message;
            }

            this.isSpinning = true;

            const intervalIds = this.matrix.map((row, rowIndex) => {
                return row.map((_, colIndex) => {
                    return this.startSpinningCell(() => {
                        this.matrix[rowIndex][colIndex] = this.getRandomSymbol();
                    });
                });
            });
            this.$refs.betLoadingSound.play();

            await new Promise(resolve => setTimeout(resolve, 3200));
            intervalIds.forEach(row => { row.forEach(clearInterval); });

            // -> verificar si ganó
            this.isSpinning = false;
            this.checkWin();
        },
        checkWin() {
            // verificar cada linea para ganar
            const lines = [
                // horizontal lines
                [this.matrix[0][0], this.matrix[0][1], this.matrix[0][2], this.matrix[0][3]],
                [this.matrix[1][0], this.matrix[1][1], this.matrix[1][2], this.matrix[1][3]],
                [this.matrix[2][0], this.matrix[2][1], this.matrix[2][2], this.matrix[2][3]],
                [this.matrix[3][0], this.matrix[3][1], this.matrix[3][2], this.matrix[3][3]],
                // vertical lines
                [this.matrix[0][0], this.matrix[1][0], this.matrix[2][0], this.matrix[3][0]],
                [this.matrix[0][1], this.matrix[1][1], this.matrix[2][1], this.matrix[3][1]],
                [this.matrix[0][2], this.matrix[1][2], this.matrix[2][2], this.matrix[3][2]],
                [this.matrix[0][3], this.matrix[1][3], this.matrix[2][3], this.matrix[3][3]],
                // diagonal lines
                [this.matrix[0][0], this.matrix[1][1], this.matrix[2][2], this.matrix[3][3]],
                [this.matrix[0][3], this.matrix[1][2], this.matrix[2][1], this.matrix[3][0]],
            ];

            for (let line of lines) {
                if (this.allEqual(line)) {
                    this.handleWin(line[0]);
                    return;
                }
            }

            this.handleLoss();
        },
        allEqual(array) {
            return array.every(val => val.name === array[0].name);
        },
        handleWin(symbol) {
            this.$refs.winSound.play();
            const winnings = this.bet * symbol.multiplier;
            this.title_bet = "Felicidades!";
            this.result = `Se agregaron S/. ${winnings} a tu cuenta.`;
            this.$store.commit('updateUserBank', this.balance + winnings);
            this.updateBalance(this.balance);
        },
        handleLoss() {
            this.result = `Quizás la próxima!`
        },
        startSpinningCell(changeCell) {
            return setInterval(changeCell, 100);
        },
        getRandomSymbol() {
            return this.symbols[Math.floor(Math.random() * this.symbols.length)];
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
    },
};
</script>
  