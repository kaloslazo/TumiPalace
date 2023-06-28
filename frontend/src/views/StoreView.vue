<template>
    <div>
        <form @submit.prevent="submit" class="max-w-lg mx-auto flex flex-col gap-10 text-white">
            <h1>Añadir fondos</h1>
            <input class="bg-brown-1000 px-6 py-3" v-model="amount" type="number" placeholder="Cantidad a añadir">
            <div class="text-white" id="card-element" />
            <button type="submit">Pagar</button>
        </form>

        <ShowError :error="error" />
        <ShowSuccess :success="success" />
    </div>
</template>
  
  
<script>
import axios from 'axios';
import { loadStripe } from '@stripe/stripe-js';

import ShowError from '@/components/ShowError.vue';
import ShowSuccess from '@/components/ShowSuccess.vue';
import { toHandlers } from 'vue';

export default {

    data() {
        return {
            stripe: null,
            card: null,
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

            try {
                const response = await axios.post('/add_funds', { amount: this.amount });
                const clientSecret = response.data.clientSecret;

                // Confirma el pago con Stripe
                const result = await this.stripe.confirmCardPayment(clientSecret, {
                    payment_method: {
                        card: this.card,
                    },
                });

                if (result.error) { this.error = result.error.message; }
                else {
                    this.success = "Pago realizado con éxito.";
                }
            } catch (error) {
                console.error("ERROR", error);
                this.error = error.response ? error.response.data.error : error.message;
            }
        },
    }
};
</script>

<style>
#card-element {
    height: 40px;
    padding: 10px;
    border: 1px solid #ccc;
}
</style>