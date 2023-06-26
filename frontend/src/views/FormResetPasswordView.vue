<template>
    <div class="bg-transparent max-w-3xl mx-auto flex flex-col items-center justify-center mt-10">
      <h2 class="text-yellow-600 font-bold text-3xl mb-10">Restablecer contraseña</h2>
      <img id="macchupicchu" class="fixed right-0 -bottom-52 -z-0" src="@/assets/img/macchuPicchuBrown.png" alt="macchu-picchu-logo">
      
      <div class="bg-brown-850 max-w-2xl w-full flex flex-col justify-center items-center rounded-md py-12">
          <div class="flex flex-row justify-center mb-12 items-center">
              <img class="h-14 w-auto mr-3" src="../assets/img/tumiLogo.png" alt="">
              <span class="mx-2 text-left text-yellow-600 font-light text-lg">
                  <h1>Tumi <br /> Palace</h1>
              </span>
          </div>
          
          <!-- Form reset -->
          <form @submit.prevent="resetPassword" class="flex flex-col justify-center- items-start gap-5 w-full max-w-sm z-10" v-if="is_updated == false">
            <div class="flex flex-col gap-2 w-full">
              <label for="password" class="text-white font-medium">Nueva contraseña</label>
              <input class="border-2 text-white border-brown-950 bg-brown-1000 py-3 px-4 focus:border-brown-950 focus:outline-0" v-model="password" type="password" placeholder="Nueva contraseña" required />
            </div>
            <div class="flex flex-col gap-2 w-full">
                <label for="password" class="text-white font-medium">Confirmar contraseña</label>
                <input class="border-2 text-white border-brown-950 bg-brown-1000 py-3 px-4 focus:border-brown-950 focus:outline-0" v-model="passwordConfirm" type="password" placeholder="Confirmar contraseña" required />
                <p class="italic text-grey-600 mt-2">* Ambas contraseñas deben coincidir.</p>
            </div>
            <button class="rounded-sm bg-yellow-600 w-full mt-5 py-2 font-medium hover:bg-yellow-700" type="submit">Restablecer contraseña</button>
          </form>
          
          <!-- Error form -->
          <div class="mt-5 bg-red-alert-bg border-t-4 border-red-alert-darker w-full max-w-sm flex flex-row py-3 px-3 z-10 items-center" v-if="error">
              <img class="h-10 w-auto" src="@/assets/svg/error.svg" alt="error-icon">
              <div class="flex flex-col ml-5">
                  <h4 class="text-red-alert-darker font-medium text-lg">Error</h4>
                  <p class="text-red-alert-darker text-sm">{{ error }}</p>
              </div>
          </div>

          <!-- Its updated form -->
          <div v-if="is_updated == true" class="max-w-md">
            <img class="h-20 w-auto mb-5 text-yellow-600" src="@/assets/svg/check.svg" alt="error-icon">
            <div class="text-white">
              <h4 class="py-3 border-b border-yellow-600">Contraseña actualizada</h4><br/>
              <h4>Tu contraseña fue actualizada con éxito. Serás redirigido a la pantalla de inicio en breves...</h4>
            </div>
          </div>

      </div>
      <div class="mt-10 text-center text-white text-sm z-10">
          <p>Regresar al <router-link class="text-yellow-600 hover:text-yellow-700 hover:underline" to="/login">Inicio de sesión</router-link></p>
      </div>
  </div>
</template>
  
<script>
import axios from 'axios';

export default {
    data() {
        return {
            password: "",
            passwordConfirm: "",
            error: "",
            is_updated: false,
        };
    },
    methods: {
        async resetPassword() {
            if (this.password !== this.passwordConfirm) {
                this.error = "Las contraseñas no coinciden.";
                return;
            }
            const token = this.$route.params.token;  // obtener el token de la URL
            try {
                const response = await axios.post(`/reset_password/${token}`, { password: this.password });
                this.error = "";
                this.is_updated = true;
                setTimeout( () => this.$router.push({ path: '/login'}), 5000);
            } catch (err) {
                this.is_updated = false;
                this.error = err.response.data.message
            }
        }
    }
};
</script>