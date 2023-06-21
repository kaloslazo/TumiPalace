<template>
  <div>
    <div class="bg-brown-950">
      <nav class="px-6 py-8 mx-auto flex items-center flex-row justify-between max-w-auto">
        <div class="flex flex-row justify-center">
          <img class="h-14 w-auto mr-3" src="../assets/img/tumiLogo.png" alt="">
          <span class="mx-2 text-center text-yellow-600 font-semibold text-xl">
            <h1>Tumi <br /> Palace</h1>
          </span>
        </div>
        <div class="flex flex-row items-center">
          <div class="flex items-center mx-5 gap-8 text-white text-lg">
            <router-link class="text-x text-white hover:text-gray-900" v-if="isLoggedIn" to="/dashboard">Games</router-link>
            <router-link class="text-x text-white hover:text-gray-900" v-if="!isLoggedIn" to="/">Home</router-link>

            <router-link to="/store">Store</router-link>
            <router-link to="/support">Support</router-link>
          </div>
          <div class="flex flex-row items-center">
            <router-link
              class="bg-transparent border-2 border-yellow-600 text-yellow-600 px-10 py-2 mx-5 rounded-sm font-medium"
              to="/login" v-if="!isLoggedIn">Login</router-link>
            <router-link class="bg-yellow-600 px-10 py-2 rounded-sm font-medium border-2 border-yellow-600" to="/register" v-if="!isLoggedIn">Register</router-link>
            
            <!-- SHOW USER CONFIG BTN -->
            <router-link to="/profile" v-if="isLoggedIn" class="flex flex-row items-center bg-brown-900 text-white mx-5 px-6 py-3 rounded-sm">
              <img 
                class="h-6 w-auto mr-4 rounded-full" 
                v-if="isLoggedIn"
                :src="user_data.imageProfile ? user_data.imageProfile : 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png'" 
                alt="user_image_profile"
              >
              <p> {{ user_data.username }} </p>
              <img class="h-4 text-yellow-600 w-auto ml-4" src="@/assets/svg/settings.svg" alt="setting-icon">
            </router-link>
             <button class="bg-yellow-600 px-10 py-2.5 rounded-sm font-medium hover:bg-yellow-700 transition-colors" @click="logout" v-if="isLoggedIn">Logout</button>
          </div>
        </div>
      </nav>
    </div>
  </div>
</template>

<script>

export default {
  computed: {
    isLoggedIn() { return this.$store.getters.isLoggedIn },
    user() { return this.$store.getters.user },
    user_data() { return this.$store.getters.user_data }
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