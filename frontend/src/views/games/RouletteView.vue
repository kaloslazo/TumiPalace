<template>
    <div class="p-6">
        <h1 class="text-3xl font-bold mb-4">Roulette</h1>
        <div class="mb-4">
            <button v-for="token in tokens" :key="token"
                :class="['p-2', 'rounded', selectedToken === token ? 'bg-red-500' : 'bg-blue-500']"
                @click="selectedToken = token">
                {{ token }}
            </button>
        </div>
        <div class="grid grid-cols-3 gap-4">
            <div v-for="number in 36" :key="number" class="flex items-center justify-between">
                <button
                    :class="['p-2', 'text-white', 'rounded', selectedNumbers.includes(number) ? 'bg-red-500' : 'bg-blue-500']"
                    @click="placeBet(number)">
                    {{ number }}
                </button>
            </div>
        </div>
        <!-- TODO: Add the buttons for the other bet types -->
    </div>
</template>
  
<script>
import axios from 'axios'

export default {
    data() {
        return {
            selectedToken: [],
            tokens: [5, 10, 15],
            result: null,
            betting: false
        }
    },
    methods: {
        async placeBet(number) {
            if (!this.selectedToken) {
                alert('Please select a token before placing a bet.')
                return
            }
            this.betting = true
            const betData = [{ type: 'number', value: number, amount: this.selectedToken }]
            const response = await axios.post('/api/roulette/bet', { bet_data: betData })
            // TODO: Handle the response, show the result to the user
            this.betting = false
        }
    }
}
</script>
  