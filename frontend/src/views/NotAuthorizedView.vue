<template>
    <div>
        <h1>Not Authorized</h1>
        <p>You are not authorized to view this page.</p>
        <button @click="moveLogin">Login</button>
    </div>
</template>

<script>
export default {
    methods: {
        moveLogin() { this.$router.push({ name: 'login' }); }
    }
}
</script>