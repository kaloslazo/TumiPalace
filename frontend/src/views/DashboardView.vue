<template>
    <div class="w-full max-w-full px-6 flex flex-col gap-5">
        <!-- portada -->
        <h2 class="text-white border-b-2 border-yellow-600 py-5 mb-10 font-semibold text-2xl">Juegos disponibles</h2>
        
        <!-- Iteration por cada juego -->
        <div class="flex flex-row gap-10 flex-wrap">
            <div v-if="loading">
                <p class="text-white">Cargando juegos...</p>
            </div>
            <router-link v-else v-for="game in games" :key="game.id" :to="`/games/${game.alias}`" class="bg-brown-1000 py-10 px-5 max-w-xs block border-2 border-transparent hover:border-yellow-600 transition-all rounded-md">
                <div class="hero-pattern bg-yellow-800 text-center relative">
                  <div class="relative z-10 flex items-center justify-center">
                    <img :src="getImageUrl(game.imageGame)" alt="imagen de juego" class="mx-auto w-36"/>
                  </div>
                </div>
                <h2 class="text-white font-semibold text-xl my-5 py-2 border-b-2 border-yellow-600">{{ game.name }}</h2>
                <p class="text-grey-400">{{ game.description }}</p>
            </router-link>
        </div>
    </div>
</template>

<style>
.hero-pattern {
    position: relative;
    background-color: #382c27;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='32' height='32' viewBox='0 0 32 32'%3E%3Cg fill-rule='evenodd'%3E%3Cg id='Artboard-5' fill='%23fbbf24' fill-opacity='0.25' fill-rule='nonzero'%3E%3Cpath d='M6 18h12V6H6v12zM4 4h16v16H4V4z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    background-repeat: repeat;
  }
  .hero-pattern::before {
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background: #382c274d;
  }
</style>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            games: [],
            loading: true,
        };
    },
    computed: {
        isLoggedIn() {
            return this.$store.getters.isLoggedIn
        },
        user() {
            return this.$store.getters.user
        }
    },
    async mounted() {
        try {
            const response = await axios.get('/games');
            this.games = response.data;
        } finally {
            this.loading = false;
        }
    },
    methods: {
        getImageUrl(imagePath) {
            return `http://127.0.0.1:5004/api/${imagePath}`;
        },
    }
}
</script>