<template>
    <div>
        <h1>Dashboard</h1>
        <button v-if="isLoggedIn" @click="logout">Logout</button>
        <p>Is logged in: {{ isLoggedIn }}</p>
    </div>
</template>

<script>
export default {
    computed: {
        isLoggedIn() {
            return this.$store.getters.isLoggedIn
        },
        user() {
            return this.$store.getters.user
        }
    },
    methods: {
        async logout() {
            try {
                await this.$store.dispatch('logout')
                this.$router.push('/login')
            } catch (err) {
                this.error = err.message
            }
        }
    }
}
</script>