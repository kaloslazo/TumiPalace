<!-- LoginForm logic -->
<template>
    <div class="bg-transparent max-w-3xl mx-auto flex flex-col items-center justify-center mt-10">
        <h2 class="text-yellow-600 font-bold text-3xl mb-10">Iniciar sesión</h2>
        <img id="macchupicchu" class="fixed right-0 -bottom-52 -z-0" src="@/assets/img/macchuPicchuBrown.png" alt="macchu-picchu-logo">
        
        <div class="bg-brown-850 max-w-2xl w-full flex flex-col justify-center items-center rounded-md py-12">
            <div class="flex flex-row justify-center mb-12 items-center">
                <img class="h-14 w-auto mr-3" src="@/assets/img/tumiLogo.png" alt="">
                <span class="mx-2 text-left text-yellow-600 font-light text-lg">
                    <h1>Tumi <br /> Palace</h1>
                </span>
            </div>
            
            <form @submit.prevent="login" class="flex flex-col justify-center- items-start gap-5 w-full max-w-sm z-10">
                <div class="flex flex-col gap-2 w-full">
                    <label for="nickname" class="text-white font-medium">Nickname</label>
                    <input class="border-2 text-white border-brown-950 bg-brown-1000 py-3 px-4 focus:border-brown-950 focus:outline-0" type="text" v-model="username" placeholder="Nickname" required />
                </div>
                <div class="flex flex-col gap-2 w-full">
                    <label for="nickname" class="text-white font-medium">Contraseña</label>
                    <input class="border-2 text-white border-brown-950 bg-brown-1000 py-3 px-4 focus:border-brown-950 focus:outline-0" type="password" v-model="password" placeholder="Contraseña" required />
                    <p class="mt-2"><router-link class="text-yellow-600 hover:text-yellow-700 hover:underline text-sm" to="/reset_password">Olvidaste tu contraseña?</router-link></p>
                </div>
                <button class="rounded-sm bg-yellow-600 w-full mt-8 py-2 font-medium" type="submit">Ingresa</button>
            </form>
            
            <div class="mt-5 bg-red-alert-bg border-t-4 border-red-alert-darker w-full max-w-sm flex flex-row py-3 px-3 z-10 items-center" v-if="error">
                <img class="h-10 w-auto" src="@/assets/svg/error.svg" alt="error-icon">
                <div class="flex flex-col ml-5">
                    <h4 class="text-red-alert-darker font-medium text-lg">Error</h4>
                    <p class="text-red-alert-darker text-sm">{{ error }}</p>
                </div>
            </div>
            
        </div>
        <div class="mt-10 text-center text-white text-sm z-10">
            <p>Aún no tienes una cuenta? <router-link class="text-yellow-600 hover:text-yellow-700 hover:underline" to="/register">Regístrate</router-link></p>
            <br/>
            <p>Regresar al <router-link class="text-yellow-600 hover:text-yellow-700 hover:underline" to="/">Inicio</router-link></p>
        </div>
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
                this.$router.push('/dashboard')
            } catch (err) {
                this.error = err.response.data.message;
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
    created() {
        document.title = "Login | TumiPalace";
    },
};
</script>

<style>
#macchupicchu {
  width: 550px;
}
</style>