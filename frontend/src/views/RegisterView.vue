<!-- RegisterForm logic -->
<template>
    <div>
        <form @submit.prevent="register">
            <input v-model="username" type="text" placeholder="Username" required>
            <input v-model="password" type="password" placeholder="Password" required>
            <input v-model="email" type="email" placeholder="Email" required>
            <input v-model="age" type="number" placeholder="Age" required>
            <button type="submit">Register</button>
        </form>
        <hr>
        <p v-if="error">{{ error }}</p>
    </div>
</template>


<!-- Handle script -->
<script>
import createUserApi from '@/services/createUser.api.js';

export default {
    data() {
        return {
            username: "",
            password: "",
            email: "",
            age: "",
            error: ""
        };
    },
    methods: {
        async register() {
            this.error = "";
            try {
                const response = await createUserApi.registerUser(
                    this.username, 
                    this.password, 
                    this.email, 
                    this.age
                );
                this.$router.push('/login');
                console.log(response);
            } catch (err) {
                if (err.response) { this.error = err.response.data.message;}
                else if (err.request) { this.error = 'No response from server';}
                else { this.error = 'Error: ' + err.message; }
            }
        },
    },
};
</script>
  