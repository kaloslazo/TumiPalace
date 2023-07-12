<template>
    <div class="px-6 max-w-2xl mx-auto">
        <div class="w-full max-w-2xl bg-brown-1000">
            <form @submit.prevent="submit" class="bg-gray-900 text-white rounded-lg p-8 max-w-lg m-auto py-24">
                <h1 class="text-3xl font-bold mb-8">Añadir fondos</h1>
                
                <label for="amount">Ingresar monto S/.</label>
                <input class="bg-white px-6 py-3 rounded-md text-black w-full mb-6 mt-5" v-model="amount" type="number"
                    placeholder="Cantidad a añadir" />
                
                <label for="card-element">Datos bancarios</label>
                <div id="card-element" class="p-2 bg-white text-black rounded-md py-5 mb-6 mt-5"></div>
                
                <button :disabled="processing"
                    class="w-full bg-yellow-600 hover:bg-yellow-700 text-black font-bold py-3 rounded-md transition duration-300"
                    type="submit">
                    Pagar
                </button>
            </form>
        </div>

        <ShowError :error="error" />
        <ShowSuccess :success="success" />
    </div>
</template>
  
<script>
import axios from 'axios';
import { loadStripe } from '@stripe/stripe-js';

import ShowError from '@/components/ShowError.vue';
import ShowSuccess from '@/components/ShowSuccess.vue';

export default {
    data() {
        return {
            stripe: null,
            card: null,
            processing: false,
            publishableKey: process.env.VUE_APP_STRIPE_PUBLIC_KEY,
            amount: 0,
            success: "",
            error: "",
        };
    },
    async mounted() {
        this.stripe = await loadStripe(this.publishableKey);
        const elements = this.stripe.elements();
        this.card = elements.create('card');
        this.card.mount('#card-element');
    },
    components: {
        ShowError,
        ShowSuccess
    },
    methods: {
        async submit() {
            this.success = "";
            this.error = "";
            this.processing = true;

            try {
                const response = await axios.post('/add_funds', { amount: this.amount });
                const clientSecret = response.data.clientSecret;

                const result = await this.stripe.confirmCardPayment(clientSecret, {
                    payment_method: {
                        card: this.card,
                    },
                });

                if (result.error) {
                    this.error = result.error.message;
                } else {
                    const intervalId = setInterval(async () => {
                        const userResponse = await axios.get('/current_user');
                        const updatedBank = userResponse.data.user.bank;

                        console.log(userResponse)
                        if (updatedBank !== this.$store.state.bank) {
                            this.success = "Pago realizado con éxito.";
                            this.$store.commit('updateUserBank', updatedBank);
                            clearInterval(intervalId);
                        }
                    }, 5000);
                }
            } catch (error) {
                console.error("ERROR", error);
                this.error = error.response ? error.response.data.error : error.message;
            } finally {
                this.processing = false;
            }
        },
    }
};
</script>
  