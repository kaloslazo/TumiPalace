<template>
    <div>
        <h2>Ingresa tu nueva contraseña</h2>
        <form @submit.prevent="resetPassword">
            <input v-model="password" type="password" placeholder="Nueva contraseña" required>
            <button type="submit">Restablecer contraseña</button>
        </form>
    </div>
</template>
  
<script>
import axios from 'axios';

export default {
    data() {
        return {
            password: ""
        };
    },
    methods: {
        async resetPassword() {
            const token = this.$route.params.token;  // obtener el token de la URL
            try {
                const response = await axios.post(`/reset_password/${token}`, { password: this.password });
                console.log(response);
            } catch (error) {
                console.log(error.response);
            }
        }
    }
};
</script>