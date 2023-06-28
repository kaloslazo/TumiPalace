<template>
    <div>
        <h2 class="text-white border-b-2 border-yellow-600 py-5 mb-10 font-semibold text-2xl">Fortuna del Sol</h2>
        
        <!-- contenedor tragamonedas -->
        <div>
            <div>
                x
            </div>
                x
            <div>
                x
            </div>
                x
            <div>
                x
            </div>
        </div>
        <!-- contenedor tragamonedas -->

        <!-- imagenes -->
        <div class="flex flex-col justify-center items-center gap-4">
            <div v-for="(row, rowIndex) in matrix" :key="rowIndex" class="flex justify-center items-center gap-4">
                <div v-for="(symbol, colIndex) in row" :key="colIndex" class="text-6xl">
                <img :src="symbol.imageUrl" alt="imagen de juego" class="mx-auto w-24"/>
                </div>
            </div>
        </div>
        <!-- imagenes -->
        <div>
            <label for="bet">Apuesta: </label>
            <input id="bet" v-model.number="bet" type="number" min="1" :max="balance" />
        </div>
        <button id="btn_spin" @click="spin" :disabled=isSpinning>Girar</button>
        <p>Saldo: {{ balance }}</p>
        <p>Resultado: {{ result }}</p>

        <ShowError :error="error" />

    </div>
</template>

<style>
#btn_spin:disabled {
    cursor: not-allowed;
    opacity: 0.8;
}
.spin {
    transition: opacity 0.3s;
}
</style>

<script>
import ShowError from '@/components/ShowError.vue';
import axios from 'axios';

export default {
    data() {
        return {
            symbols: [
                { name: 'logo1', imageUrl: 'http://127.0.0.1:5004/api/static/games/slotsGame/logo1.png', multiplier: 10 },
                { name: 'logo2', imageUrl: 'http://127.0.0.1:5004/api/static/games/slotsGame/logo3.png', multiplier: 8 },
                { name: 'logo3', imageUrl: 'http://127.0.0.1:5004/api/static/games/slotsGame/logo4.png', multiplier: 5 },
            ],
            matrix: Array(3).fill().map(() => Array(3).fill(null)),
            bet: 1,
            isSpinning: false,
            result: '',
            error: '',
        }
    },
    created() {
        this.matrix = this.matrix.map(row => row.fill(this.symbols[0]));
    },
    computed: {
        user_data() { return this.$store.getters.user_data },
        balance() { return this.$store.getters.user_data.bank },
    },
    components: {
        ShowError,
    },
    methods: {
        async spin() {
            // todos los signos iguales -> x5
            // dos signos iguales -> x2
            // todos los signos distintos -> pierde la apuesta 
            
            // -> verificar apuesta
            if (this.bet < 1){ this.error = "La apuesta debe ser mayor a 1."; return; }
            if (this.bet > this.balance) { this.error = 'No tienes suficiente saldo para esta apuesta.'; return; }

            // -> actualiza el saldo
            this.$store.commit('updateUserBank', this.balance - this.bet);
            try {
                const response = await axios.post(`/users/${this.$store.getters.user_data.id}/update_balance`, { balance: this.balance });
                this.$store.commit('updateUserBank', this.balance);
                console.log(response.data.message);
            } catch (err) {
                this.error = err.response.data.message;
            }

            // -> inicia logica de giro
            this.isSpinning = true;

            const intervalIds = this.matrix.map((row, rowIndex) => {
                return row.map((_, colIndex) => {
                    return this.startSpinningCell(() => {
                        this.matrix[rowIndex][colIndex] = this.getRandomSymbol();
                    });
                });
            });

            await new Promise(resolve => setTimeout(resolve, 5000));
 
            intervalIds.forEach(row => { row.forEach(clearInterval); });
            this.isSpinning = false;
        },
        checkWin(){
            // Si no hay líneas ganadoras, el usuario pierde
        },
        handleWin(symbol){
            this.result = `Ganaste con el simbolo ${symbol}`
        },
        handleLoss(){
            this.result = `Perdiste`
        },
        startSpinningCell(changeCell) {
            return setInterval(changeCell, 100);
        },
        getRandomSymbol() {
            return this.symbols[Math.floor(Math.random() * this.symbols.length)];
        },
    },
};
</script>
  