<template>
    <form  @submit.prevent="addFunds" class="flex flex-col justify-center gap-5 mx-auto max-w-md mt-10">
        <input v-model="amount" type="number" placeholder="Cantidad a añadir">
        <input v-model="cardNumber" type="text" placeholder="Número de tarjeta">
        <input v-model="expiryDate" type="text" placeholder="Fecha de vencimiento (MM/AA)">
        <input v-model="cvc" type="text" placeholder="CVC">
        <input v-model="name" type="text" placeholder="Nombre en la tarjeta">
        <button class="mt-10" type="submit">Añadir fondos</button>
    </form >

    <ShowError :error="error"/>
    <ShowSuccess :success="success"/>

</template>
  
<script>
import axios from 'axios';
import { loadStripe } from '@stripe/stripe-js';
import ShowError from '@/components/ShowError.vue';
import ShowSuccess from '@/components/ShowSuccess.vue';

export default {
    data() {
        return {
            amount: 0,
            cardNumber: '',
            expiryDate: '',
            cvc: '',
            name: '',
            stripe: null,
            error: "",
            success: ""
        };
    },
    async created() {
        this.stripe = await loadStripe(process.env.VUE_APP_STRIPE_PUBLIC_KEY);
        console.log(process.env.VUE_APP_STRIPE_PUBLIC_KEY);
    },
    components: {
        ShowError,
        ShowSuccess
    },
    methods: {
        async addFunds() {
            try{
                this.error = "";
                const response = await axios.post('/add_funds', { amount: this.amount });
                const clientSecret = response.data.clientSecret;

                // Confirma el pago con Stripe
                const result = await this.stripe.confirmCardPayment(clientSecret, {
                    payment_method: {
                        card: {
                            number: this.cardNumber,
                            exp_month: this.expiryDate.split('/')[0],
                            exp_year: this.expiryDate.split('/')[1],
                            cvc: this.cvc,
                        },
                        billing_details: {
                            name: this.name,
                        },
                    },
                });

                this.success = "Pago realizado con exito.";
            } catch (err) {
                console.log("error", err);
                if (err.response && err.response.data) { this.error = err.response.data.message; }
                else { this.error = err.message; }
            }
        },
    },
};
</script>
  