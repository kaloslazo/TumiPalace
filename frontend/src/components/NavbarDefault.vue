<template>
  <div>
    <div class="bg-brown-950">
      <nav class="px-6 py-8 mx-auto flex items-center flex-row justify-between max-w-auto text-sm">
        <div class="flex flex-row justify-center items-center">
          <img class="h-12 w-auto mr-3" src="../assets/img/tumiLogo.png" alt="">
          <span class="mx-1 text-left text-yellow-600 font-semibold text-base"><h1>Tumi <br /> Palace</h1></span>
          <div class="flex items-center justify-center mx-5 ml-10 gap-8 text-white">
            <router-link class="text-white hover:text-grey-300 transition-all" v-if="isLoggedIn" to="/dashboard">Juegos</router-link>
            <router-link class="text-white hover:text-grey-300 transition-all" v-if="!isLoggedIn" to="/">Inicio</router-link>
            <router-link class="text-white hover:text-grey-300 transition-all" to="/store">Tienda</router-link>
            <router-link class="text-white hover:text-grey-300 transition-all" to="/support">Soporte</router-link>
          </div>
        </div>
        <div class="flex flex-row items-center">
          <div class="flex flex-row items-center">
            <router-link
              class="bg-transparent border-2 border-yellow-600 text-yellow-600 px-10 py-2 mx-5 rounded-sm font-medium text-xs hover:bg-brown-1000 transition-all"
              to="/login" v-if="!isLoggedIn">Iniciar Sesión</router-link>
            <router-link
              class="bg-yellow-600 px-10 py-2 rounded-sm font-medium border-2 border-yellow-600 hover:bg-yellow-700 text-xs hover:border-yellow-700 transition-all"
              to="/register" v-if="!isLoggedIn">Abrir Cuenta</router-link>

            <router-link to="/store" v-if="isLoggedIn">
              <p class="flex flex-row items-center justify-center gap-3 mx-5 text-white">
                <img src="@/assets/svg/coins.svg" alt="wallet icon" class="h-7 text-yellow-600 w-auto">
                S/. {{ user_data.bank }}
              </p>
            </router-link>

            <!-- SHOW USER CONFIG BTN -->
            <router-link to="/profile" v-if="isLoggedIn"
              class="flex flex-row items-center bg-brown-1000 text-white mx-5 px-6 py-2 rounded-sm text-xs">

              <img class="h-6 w-6 mr-4 rounded-full object-cover" v-if="isLoggedIn"
                :src="imageUrl"
                alt="user_image_profile">
              <p> {{ user_data.username }} </p>
              <img class="h-4 text-yellow-600 w-auto ml-4" src="@/assets/svg/settings.svg" alt="setting-icon">
            </router-link>
            <button class="bg-yellow-600 px-10 py-2.5 rounded-sm font-medium hover:bg-yellow-700 transition-colors text-xs"
              @click="logout" v-if="isLoggedIn">Logout</button>
          </div>
        </div>
      </nav>
    </div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      defaultImage: 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png',
    }
  },
  computed: {
    isLoggedIn() { return this.$store.getters.isLoggedIn },
    user() { return this.$store.getters.user },
    user_data() { return this.$store.getters.user_data },
    imageUrl() { return this.user_data.image ? `http://127.0.0.1:5004/api/${this.user_data.image}` : this.defaultImage }
  },
  methods: {
    logout() {
      this.$store.dispatch('logout')
        .then(() => { this.$router.push('/login'); })
        .catch(err => { console.error(err); });
    }
  },
  watch: {
    $route(to, from) {
      document.title = (to.meta.title ? to.meta.title : 'Home') + " | TumiPalace";
    },
  },
  created() {
    document.title = (this.$route.meta.title ? this.$route.meta.title : 'Home') + " | TumiPalace";
  },
}
</script>