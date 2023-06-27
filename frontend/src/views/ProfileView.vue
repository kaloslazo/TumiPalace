<template>
    <div class="flex lg:flex-row flex-col mx-auto px-6 mt-5 w-full gap-10 lg:gap-0">
        <!-- start left-->
        <div class="bg-brown-1000 rounded flex flex-col w-full lg:max-w-xs py-10">
            <div class="px-12">
                <img class="h-40 w-auto mr-4 rounded-full" :src="imageUrl" alt="user_image_profile"> 
                <h2 class="font-semibold text-3xl mt-10 text-white">{{ user_data.username }}</h2>
                <h4 class="font-thin text-grey-400">{{ user_data.email }}</h4>
            </div>
            <div class="mt-10 px-6 flex flex-col items-start gap-5 text-white transition-all">
                <button class="flex flex-row hover:text-yellow-600" @click="set_personal">
                    <img class="h-5 text-yellow-600 w-auto mx-5 my-auto" src="@/assets/svg/person.svg" alt="setting-icon">
                    <span>Información Personal</span>
                </button>
                <button class="flex flex-row hover:text-yellow-600 transition-all" @click="set_security">
                    <img class="h-5 text-yellow-600 w-auto mx-5 my-auto" src="@/assets/svg/lock.svg" alt="setting-icon">
                    <span>Seguridad</span>
                </button>
                <button class="flex flex-row hover:text-yellow-600 transition-all" @click="set_membership">
                    <img class="h-5 text-yellow-600 w-auto mx-5 my-auto" src="@/assets/svg/vip_crown.svg"
                        alt="setting-icon">
                    <span>Membresía</span>
                </button>
            </div>
        </div>
        <!-- end left -->

        <!-- start right -->
        <div class="bg-brown-1000 px-12 py-10 mx-auto lg:ml-10 flex flex-col w-full lg:max-w-4xl h-auto">

            <!-- PERSONAL INFORMATION  -->
            <form @submit.prevent="updatePersonalInfo"
                class="flex flex-col justify-center- items-start gap-5 w-full max-w-sm z-10"
                v-if="personal_checked == true">
                <h2 class="text-yellow-600 font-semibold py-2 border-b-2 border-yellow-600 inline-block">Información
                    Personal</h2>
                <div class="flex flex-col gap-2 w-full">
                    <label for="nickname" class="text-white font-medium">Actualizar nickname</label>
                    <input
                        class="border-2 text-white border-brown-950 bg-brown-950 py-3 px-4 focus:border-brown-950 focus:outline-0"
                        type="text" v-model="username" placeholder="Nickname" />
                </div>

                <div class="flex flex-col gap-2 w-full">
                    <label for="nickname" class="text-white font-medium">Actualizar correo electrónico</label>
                    <input
                        class="border-2 text-white border-brown-950 bg-brown-950 py-3 px-4 focus:border-brown-950 focus:outline-0"
                        v-model="email" type="email" placeholder="Correo electrónico" />
                </div>

                <div class="flex flex-col gap-2 w-full">
                    <label for="imageProfile" class="text-white font-medium">Actualizar imagen de perfil:</label>
                    <input
                        class="border-2 text-white border-brown-950 bg-brown-950 py-3 px-4 focus:border-brown-950 focus:outline-0"
                        type="file" id="imageProfile" name="imageProfile" accept="image/*" @change="onFileChange">
                </div>

                <ShowError v-bind:error="error" />

                <p class="flex flex-row gap-5 mt-5 w-full">
                    <button class="rounded-sm bg-red-600 w-full py-2 font-medium text-sm" type="submit">Eliminar
                        cuenta</button>
                    <button class="rounded-sm bg-yellow-600 w-full py-2 font-medium text-sm" type="submit">Guardar
                        cambios</button>
                </p>
            </form>

            <!-- SECURITY -->
            <form @submit.prevent="updateSecurity"
                class="flex flex-col justify-center- items-start gap-5 w-full max-w-sm z-10" v-if="security_checked">
                <h2 class="text-yellow-600 font-semibold py-2 border-b-2 border-yellow-600 inline-block">Seguridad</h2>
                <div class="flex flex-col gap-2 w-full">
                    <label for="nickname" class="text-white font-medium">Contraseña actual</label>
                    <input
                        class="border-2 text-white border-brown-950 bg-brown-950 py-3 px-4 focus:border-brown-950 focus:outline-0"
                        v-model="password" type="password" placeholder="Contraseña actual" />
                </div>

                <div class="flex flex-col gap-2 w-full">
                    <label for="nickname" class="text-white font-medium">Nueva contraseña</label>
                    <input
                        class="border-2 text-white border-brown-950 bg-brown-950 py-3 px-4 focus:border-brown-950 focus:outline-0"
                        v-model="password" type="password" placeholder="Nueva contraseña" />
                </div>

                <ShowError v-bind:error="error" />

                <p class="flex flex-row gap-5 mt-5 w-full">
                    <button class="rounded-sm bg-red-600 w-full py-2 font-medium text-sm" type="submit">Eliminar
                        cuenta</button>
                    <button class="rounded-sm bg-yellow-600 w-full py-2 font-medium text-sm" type="submit">Guardar
                        cambios</button>
                </p>
            </form>

            <!-- MEMBERSHIP -->
            <form @submit.prevent="updateMembership"
                class="flex flex-col justify-center- items-start gap-5 w-full max-w-sm z-10"
                v-if="membership_checked == true">
                <h2 class="text-yellow-600 font-semibold py-2 border-b-2 border-yellow-600 inline-block">Membresía</h2>
                <div class="flex flex-col gap-2 w-full">
                    <label for="nickname" class="text-white font-medium">Contraseña actual</label>
                    <input
                        class="border-2 text-white border-brown-950 bg-brown-950 py-3 px-4 focus:border-brown-950 focus:outline-0"
                        v-model="password" type="password" placeholder="Contraseña actual" />
                </div>

                <div class="flex flex-col gap-2 w-full">
                    <label for="nickname" class="text-white font-medium">Nueva contraseña</label>
                    <input
                        class="border-2 text-white border-brown-950 bg-brown-950 py-3 px-4 focus:border-brown-950 focus:outline-0"
                        v-model="password" type="password" placeholder="Nueva contraseña" />
                </div>

                <!-- <ShowError v-bind:error="error" /> -->
                <!-- Error form -->
                <div class="mt-5 bg-red-alert-bg border-t-4 border-red-alert-darker w-full max-w-sm flex flex-row py-3 px-3 z-10 items-center" v-if="error">
                    <img class="h-10 w-auto" src="@/assets/svg/error.svg" alt="error-icon">
                    <div class="flex flex-col ml-5">
                        <h4 class="text-red-alert-darker font-medium text-lg">Error</h4>
                        <p class="text-red-alert-darker text-sm">{{ error }}</p>
                    </div>
                </div>

                <p class="flex flex-row gap-5 mt-5 w-full">
                    <button class="rounded-sm bg-red-600 w-full py-2 font-medium text-sm" type="submit">Eliminar
                        cuenta</button>
                    <button class="rounded-sm bg-yellow-600 w-full py-2 font-medium text-sm" type="submit">Guardar
                        cambios</button>
                </p>
            </form>

            <img :src=imageUrl alt="">

        </div>
        <!-- end left -->
    </div>
</template>

<script>
import axios from 'axios';
import ShowError from '@/components/ShowError.vue';

export default {
    data() {
        return {
            personal_checked: true,
            security_checked: false,
            membership_checked: false,
            error: "",
            username: "",
            email: "",
            password: "",
            imageProfile: null,
            defaultImage: 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png'
        }
    },
    computed: {
        user_data() { return this.$store.getters.user_data },
        imageUrl() { return this.user_data.image ? `http://127.0.0.1:5004/api/${this.user_data.image}` : this.defaultImage; },
    },
    methods: {
        async mounted() {
            const token = localStorage.getItem('token');
            const response = await axios.get('/current_user', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            console.log(response.data);
            if (response.data.status === 'authenticated') { this.$store.commit('updateUser', response.data); }
        },
        set_personal() {
            this.security_checked = false;
            this.membership_checked = false;
            this.personal_checked = true;
        },
        set_security() {
            this.personal_checked = false;
            this.membership_checked = false;
            this.security_checked = true;
        },
        set_membership() {
            this.personal_checked = false;
            this.security_checked = false;
            this.membership_checked = true;
        },
        async updatePersonalInfo() {
            const userId = this.$store.getters.user_data.id;

            try {
                let formData = new FormData();
                if (this.username != "") { formData.append('username', this.username); }
                if (this.email != "") { formData.append('email', this.email); }
                if (this.imageProfile != null) { formData.append('imageProfile', this.imageProfile); }

                await axios.put(`/users/${userId}`, formData, {
                    headers: { 'Content-Type': 'multipart/form-data' }
                });

                const response_updated = await axios.get(`/users/${userId}`);
                this.$store.commit('updateUser', response_updated.data);
            } catch (err) { 
                this.error = err.response.data.message
            }
        },
        async updateSecurity() {
            // Implementar la lógica para actualizar la seguridad aquí
        },
        async updateMembership() {
            // Implementar la lógica para actualizar la membresía aquí
        },
        onFileChange(e) {
            const file = e.target.files[0];
            this.imageProfile = file;
        },
    },
}
</script>