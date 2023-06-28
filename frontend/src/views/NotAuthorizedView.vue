<template>
    <div class="w-full mx-auto text-center max-w-xl">
        <div class="flex flex-col items-center w-auto">
            <img class="h-28 text-center mx-auto text-yellow-600 w-auto mt-20" src="@/assets/svg/security.svg" alt="setting-icon">
            <h1 class="text-white font-bold text-3xl mt-16">Página no disponible</h1>
            <p class="text-grey-400 my-3 text-lg">Lo sentimos, no estás autorizado para acceder a esta página.</p>
        </div>
        <p class="text-white mt-10">Regresar al <router-link class="text-yellow-600 hover:text-yellow-700 hover:underline" to="/">Inicio</router-link></p>
    </div>
</template>

<script>
export default {
    methods: {
        moveLogin() { this.$router.push({ name: 'login' }); }
    }
}
</script>