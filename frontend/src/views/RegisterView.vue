<!-- RegisterForm logic -->
<template>
    <div class="bg-transparent max-w-3xl mx-auto flex flex-col items-center justify-center mt-10">
        <h2 class="text-yellow-600 font-bold text-3xl mb-10">Abrir Cuenta</h2>
        <img id="macchupicchu" class="fixed right-0 -bottom-52 -z-0" src="@/assets/img/macchuPicchuBrown.png" alt="macchu-picchu-logo">
        
        <div class="bg-brown-850 max-w-2xl w-full flex flex-col justify-center items-center rounded-md py-12">
            <div class="flex flex-row justify-center mb-12 items-center">
                <img class="h-14 w-auto mr-3" src="../assets/img/tumiLogo.png" alt="">
                <span class="mx-2 text-left text-yellow-600 font-light text-lg">
                    <h1>Tumi <br /> Palace</h1>
                </span>
            </div>
            <!-- start form -->
            <form @submit.prevent="register" class="flex flex-col justify-center- items-start gap-5 w-full max-w-sm z-10">
                <div class="flex flex-col gap-2 w-full">
                    <label for="nickname" class="text-white font-medium">Nickname</label>
                    <input class="border-2 text-white border-brown-950 bg-brown-1000 py-3 px-4 focus:border-brown-950 focus:outline-0" type="text" v-model="username" placeholder="Nickname" required />
                </div>

                <div class="flex flex-col gap-2 w-full">
                    <label for="nickname" class="text-white font-medium">Contraseña</label>
                    <input class="border-2 text-white border-brown-950 bg-brown-1000 py-3 px-4 focus:border-brown-950 focus:outline-0" v-model="password" type="password" placeholder="Contraseña" required/>
                </div>

                <div class="flex flex-col gap-2 w-full">
                    <label for="nickname" class="text-white font-medium">Correo electrónico</label>
                    <input class="border-2 text-white border-brown-950 bg-brown-1000 py-3 px-4 focus:border-brown-950 focus:outline-0" v-model="email" type="email" placeholder="Correo electrónico" required/>
                </div>
                
                <div class="flex items-start gap-2 w-full">
                    <input id="age_verification" class="mt-1 border-2 text-white border-brown-950 bg-brown-1000 py-3 px-4 focus:border-brown-950 focus:outline-0" type="checkbox" required/>
                    <label for="age_verification" class="text-white font-thin text-xs">Soy mayor de 18 años y acepto los <router-link to="terms" class="underline">Términos</router-link> y la <router-link to="privacy" class="underline">Política de Privacidad.</router-link></label>
                </div>

                <button class="rounded-sm bg-yellow-600 w-full mt-8 py-2 font-medium" type="submit">Regístrate</button>
            </form>
            <!-- start form -->


            <!-- start error div -->
            <div class="mt-5 bg-red-alert-bg border-t-4 border-red-alert-darker w-full max-w-sm flex flex-row py-3 px-3 z-10 items-center" v-if="error">
                <img class="h-10 w-auto" src="@/assets/svg/error.svg" alt="error-icon">
                <div class="flex flex-col ml-5">
                    <h4 class="text-red-alert-darker font-medium text-lg">Error</h4>
                    <p class="text-red-alert-darker text-sm">{{ error }}</p>
                </div>
            </div>
            <!-- end error div -->
        </div>
        <!-- start seconday messages -->
        <div class="mt-10 text-center text-white text-sm z-10">
            <p>Ya tienes una cuenta? <router-link class="text-yellow-600 hover:text-yellow-700 hover:underline" to="/login">Inicia Sesión</router-link></p>
            <br/>
            <p>Regresar al <router-link class="text-yellow-600 hover:text-yellow-700 hover:underline" to="/">Inicio</router-link></p>
        </div>
        <!-- end seconday messages -->
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
                );
                this.$router.push('/login');
                console.log(response);
            } catch (err) {
                if (err.response) { this.error = err.response.data.message; }
                else if (err.request) { this.error = 'No response from server'; }
                else { this.error = 'Error: ' + err.message; }
            }
        },
    },
    created() {
        document.title = "Register | TumiPalace";
    },
};
</script>
  