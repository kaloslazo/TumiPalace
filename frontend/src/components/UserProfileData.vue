<template>
    <div>
        Usuario: {{  user.username }}
    </div>
</template>


<script>
export default {
    computed: {
        user() {
            return this.$store.getters.user
        }
    }
}
</script>