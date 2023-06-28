<template>
    <div class="flex lg:flex-row flex-col mx-auto px-6 mt-5 w-full gap-10 lg:gap-0">
        <!-- start left-->
        <div class="bg-brown-1000 rounded flex flex-col w-full lg:max-w-xs py-10">
            <div class="px-12">
                <img class="h-40 w-40 mr-4 rounded-full object-cover" :src="imageUrl" alt="user_image_profile"> 
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
                    <img class="h-5 text-yellow-600 w-auto mx-5 my-auto" src="@/assets/svg/vip_crown.svg" alt="setting-icon">
                    <span>Membresía</span>
                </button>
                <button class="flex flex-row hover:text-yellow-600 transition-all" @click="set_delete_account">
                    <img class="h-5 text-yellow-600 w-auto mx-5 my-auto" src="@/assets/svg/delete.svg" alt="setting-icon">
                    <span>Eliminar cuenta</span>
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
                        type="file" id="imageProfile" name="imageProfile" accept="image/*" @change="onFileChange" ref="fileInput">
                </div>

                <ShowError v-bind:error="error" />
                <ShowSuccess v-bind:success="success" />

                <p class="flex flex-row gap-5 mt-5 w-full">
                    <button class="rounded-sm bg-yellow-600 w-full py-2 font-medium text-sm" type="submit">Guardar
                        cambios</button>
                </p>
            </form>

            <!-- SECURITY -->
            <form @submit.prevent="updateSecurity"
                class="flex flex-col justify-center- items-start gap-5 w-full max-w-sm z-10" v-if="security_checked">
                <h2 class="text-yellow-600 font-semibold py-2 border-b-2 border-yellow-600 inline-block">Seguridad</h2>
                <div class="flex flex-col gap-2 w-full">
                    <label for="pass" class="text-white font-medium">Contraseña actual</label>
                    <input
                        class="border-2 text-white border-brown-950 bg-brown-950 py-3 px-4 focus:border-brown-950 focus:outline-0"
                        v-model="password" type="password" placeholder="Contraseña actual" />
                </div>

                <div class="flex flex-col gap-2 w-full">
                    <label for="new_pass" class="text-white font-medium">Nueva contraseña</label>
                    <input
                        class="border-2 text-white border-brown-950 bg-brown-950 py-3 px-4 focus:border-brown-950 focus:outline-0"
                        v-model="new_password" type="password" placeholder="Nueva contraseña" />
                </div>

                <ShowError v-bind:error="error" />
                <ShowSuccess v-bind:success="success" />

                <p class="flex flex-row gap-5 mt-5 w-full">
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
                    <label for="pass" class="text-white font-medium">Contraseña actual</label>
                    <input
                        class="border-2 text-white border-brown-950 bg-brown-950 py-3 px-4 focus:border-brown-950 focus:outline-0"
                        v-model="password" type="password" placeholder="Contraseña actual" />
                </div>

                <div class="flex flex-col gap-2 w-full">
                    <label for="newpass" class="text-white font-medium">Nueva contraseña</label>
                    <input
                        class="border-2 text-white border-brown-950 bg-brown-950 py-3 px-4 focus:border-brown-950 focus:outline-0"
                        v-model="new_password" type="password" placeholder="Nueva contraseña" />
                </div>

                <ShowError v-bind:error="error" />

                <p class="flex flex-row gap-5 mt-5 w-full">
                    <button class="rounded-sm bg-yellow-600 w-full py-2 font-medium text-sm" type="submit">Guardar
                        cambios</button>
                </p>
            </form>

            <!-- DELETE ACCOUNT -->
            <form @submit.prevent="deleteUser"
                class="flex flex-col justify-center items-start gap-5 w-full max-w-sm z-10" v-if="delete_account_checked == true">
                <h2 class="text-yellow-600 font-semibold py-2 border-b-2 border-yellow-600 inline-block">Eliminar cuenta</h2>
                <p class="text-white">Estás seguro que quieres eliminar tu cuenta? Esta acción no se puede deshacer.</p>
                
                <div class="flex flex-col gap-2 w-full">
                    <label for="nickname" class="text-white font-medium">Contraseña</label>
                    <input class="border-2 text-white border-brown-950 bg-brown-950 py-3 px-4 focus:border-brown-950 focus:outline-0" v-model="password" type="password" placeholder="Contraseña actual" />
                    <!-- checkbox accept delete -->
                    <div class="flex items-start gap-2 w-full mt-5">
                        <input id="age_verification" class="mt-1 border-2 text-white border-brown-950 bg-brown-1000 py-3 px-4 focus:border-brown-950 focus:outline-0" type="checkbox" required/>
                        <label for="age_verification" class="text-white font-thin text-xs">Acepto que al eliminar mi cuenta todo mi progreso se perderá y es irrecuperable.</label>
                    </div>
                </div>
                
                <ShowError v-bind:error="error" />
                <ShowSuccess v-bind:success="success" />

                <p class="flex flex-row gap-5 mt-5 w-full">
                    <button class="rounded-sm bg-yellow-600 w-full py-2 font-medium text-sm" type="submit">Eliminar cuenta</button>
                    <button class="rounded-sm bg-red-600 w-full py-2 font-medium text-sm" type="button" @click="cancelDelete">Cancelar</button>
                </p>
            </form>
        </div>
        <!-- end left -->
    </div>
</template>

<script>
import axios from 'axios';
import ShowError from '@/components/ShowError.vue';
import ShowSuccess from '@/components/ShowSuccess.vue';

export default {
    components: {
        ShowError,
        ShowSuccess
    },
    data() {
        return {
            personal_checked: true,
            security_checked: false,
            membership_checked: false,
            delete_account_checked: false,
            success: "",
            error: "",
            username: "",
            email: "",
            password: "",
            new_password: "",
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
            this.delete_account_checked = false;
            this.error = "";
            this.success = "";
        },
        set_security() {
            this.personal_checked = false;
            this.membership_checked = false;
            this.security_checked = true;
            this.delete_account_checked = false;
            this.success = "";
            this.error = "";
        },
        set_membership() {
            this.personal_checked = false;
            this.security_checked = false;
            this.membership_checked = true;
            this.delete_account_checked = false;
            this.error = "";
            this.success = "";
        },
        set_delete_account(){
            this.personal_checked = false;
            this.security_checked = false;
            this.membership_checked = false;
            this.delete_account_checked = true;
            this.error = "";
            this.success = "";
        },
        // methods async
        async deleteAccount(){

        },
        async updatePersonalInfo() {
            const userId = this.$store.getters.user_data.id;

            try {
                this.error = "";
                this.success = "";
                let formData = new FormData();
                if (this.username != "") { formData.append('username', this.username); }
                if (this.email != "") { formData.append('email', this.email); }
                if (this.imageProfile != null) { formData.append('imageProfile', this.imageProfile); }

                const response = await axios.put(`/users/${userId}`, formData, {
                    headers: { 'Content-Type': 'multipart/form-data' }
                });

                const response_updated = await axios.get(`/users/${userId}`);

                this.$store.commit('updateUser', {
                    image: response_updated.data.imageProfile,
                    username: response_updated.data.nickname,
                    email: response_updated.data.email
                });

                this.success = "Actualizado correctamente";

                // Limpiar los campos de entrada
                this.username = "";
                this.email = "";
                this.imageProfile = null;
                this.$refs.fileInput.value = null;
            } catch (err) { 
                this.error = err.response.data.message
            }
        },
        async deleteUser(){
            try {
                this.error = "";
                this.success = "";

                const userID = this.$store.getters.user_data.id;
                const response = await axios.delete(`/users/${userID}`, {
                    data: { password: this.password }
                });

                this.success = response.data.message;
                
                // despues de 5 segundos...
                setTimeout(() => {
                    this.$store.commit('logout');
                    this.$router.push('/login');
                }, 3000);
            } catch (err) {
                this.error = err.response.data.message;
            }
        },
        async updateSecurity() {
            // Implementar la lógica para actualizar la seguridad aquí
            const userId = this.$store.getters.user_data.id;
            try {
                this.error = "";
                this.success = "";

                const response = await axios.post(`/users/${userId}/change_password`, { password: this.password, new_password: this.new_password });

                this.success = response.data.message;
                
                // Limpiar los campos de entrada
                this.new_password = "";
                this.password = "";
            } catch (err) { 
                this.error = err.response.data.message
            }
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