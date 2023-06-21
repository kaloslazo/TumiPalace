<!-- LoginForm logic -->
<template>
    <div>
        <form @submit.prevent="login">
            <input type="text" v-model="username" placeholder="Username" required />
            <input type="password" v-model="password" placeholder="Password" required />
            <button type="submit">Login</button>
        </form>
        <hr />
        <p v-if="error">{{ error }}</p>
        <hr />
        <p>Is logged in: {{ isLoggedIn }}</p>
    </div>
</template>


<!-- Script logic -->
<script>
export default {
    data() {
        return {
            username: "",
            password: "",
            error: ""
        };
    },
    methods: {
        async login() {
            const user = {
                username: this.username,
                password: this.password
            }
            try {
                await this.$store.dispatch('login', user)
                // this.$router.push('/dashboard')
            } catch (err) {
                this.error = err.message
            }
        }
    },
    computed: {
        isLoggedIn() {
            return this.$store.getters.isLoggedIn
        },
        user() {
            return this.$store.getters.user
        }
    },
};
</script>