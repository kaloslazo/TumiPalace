<template>
    <div>
        <h1>Dashboard</h1>
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