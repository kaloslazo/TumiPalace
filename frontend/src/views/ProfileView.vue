<template>
    <div class="flex lg:flex-row flex-col mx-auto px-6 mt-5 w-full">
        <!-- start left-->
        <div class="bg-brown-1000 rounded flex flex-col w-full max-w-sm py-10">
            <div class="px-12">
                <img class="h-40 w-auto mr-4 rounded-full" :src="user_data.imageProfile ? user_data.imageProfile : 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png'" alt="user_image_profile" >
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
            </div>
        </div>
        <!-- end left -->

        <!-- start right -->
        <div class="bg-brown-1000 pl-6 py-10 mx-auto ml-10 flex flex-col w-full max-w-4xl h-auto">

            <!-- PERSONAL INFORMATION  -->
            <form @submit.prevent="register" class="flex flex-col justify-center- items-start gap-5 w-full max-w-sm z-10" v-if="personal_checked == true">
                <h2 class="text-yellow-600 font-semibold py-2 border-b-2 border-yellow-600 inline-block">Información Personal</h2>
                <div class="flex flex-col gap-2 w-full">
                    <label for="nickname" class="text-white font-medium">Nickname</label>
                    <input class="border-2 text-white border-brown-950 bg-brown-1000 py-3 px-4 focus:border-brown-950 focus:outline-0" type="text" v-model="username" placeholder="Nickname" required />
                </div>

                <div class="flex flex-col gap-2 w-full">
                    <label for="nickname" class="text-white font-medium">Actualizar correo electrónico</label>
                    <input class="border-2 text-white border-brown-950 bg-brown-1000 py-3 px-4 focus:border-brown-950 focus:outline-0" v-model="email" type="email" placeholder="Correo electrónico" required/>
                </div>
                <p class="flex flex-row gap-5 mt-5 w-full">
                    <button class="rounded-sm bg-red-600 w-full py-2 font-medium" type="submit">Eliminar cuenta</button>
                    <button class="rounded-sm bg-yellow-600 w-full py-2 font-medium" type="submit">Guardar cambios</button>
                </p>
            </form>
            
            <!-- SECURITY -->
            <form @submit.prevent="register" class="flex flex-col justify-center- items-start gap-5 w-full max-w-sm z-10" v-if="security_checked">
                <h2 class="text-yellow-600 font-semibold py-2 border-b-2 border-yellow-600 inline-block">Seguridad</h2>
                <div class="flex flex-col gap-2 w-full">
                    <label for="nickname" class="text-white font-medium">Contraseña actual</label>
                    <input class="border-2 text-white border-brown-950 bg-brown-1000 py-3 px-4 focus:border-brown-950 focus:outline-0" v-model="password" type="password" placeholder="Contraseña actual" required/>
                </div>
                
                <div class="flex flex-col gap-2 w-full">
                    <label for="nickname" class="text-white font-medium">Nueva contraseña</label>
                    <input class="border-2 text-white border-brown-950 bg-brown-1000 py-3 px-4 focus:border-brown-950 focus:outline-0" v-model="password" type="password" placeholder="Nueva contraseña" required/>
                </div>
                <p class="flex flex-row gap-5 mt-5 w-full">
                    <button class="rounded-sm bg-red-600 w-full py-2 font-medium" type="submit">Eliminar cuenta</button>
                    <button class="rounded-sm bg-yellow-600 w-full py-2 font-medium" type="submit">Guardar cambios</button>
                </p>
            </form>

            <!-- MEMBERSHIP -->
            <form @submit.prevent="register" class="flex flex-col justify-center- items-start gap-5 w-full max-w-sm z-10" v-if="membership_checked == true">
                <h2 class="text-yellow-600 font-semibold py-2 border-b-2 border-yellow-600 inline-block">Membresía</h2>
                <div class="flex flex-col gap-2 w-full">
                    <label for="nickname" class="text-white font-medium">Contraseña actual</label>
                    <input class="border-2 text-white border-brown-950 bg-brown-1000 py-3 px-4 focus:border-brown-950 focus:outline-0" v-model="password" type="password" placeholder="Contraseña actual" required/>
                </div>
                
                <div class="flex flex-col gap-2 w-full">
                    <label for="nickname" class="text-white font-medium">Nueva contraseña</label>
                    <input class="border-2 text-white border-brown-950 bg-brown-1000 py-3 px-4 focus:border-brown-950 focus:outline-0" v-model="password" type="password" placeholder="Nueva contraseña" required/>
                </div>
                <p class="flex flex-row gap-5 mt-5 w-full">
                    <button class="rounded-sm bg-red-600 w-full py-2 font-medium" type="submit">Eliminar cuenta</button>
                    <button class="rounded-sm bg-yellow-600 w-full py-2 font-medium" type="submit">Guardar cambios</button>
                </p>
            </form>

        </div>
        <!-- end left -->
    </div>
</template>

<script>
export default {
    data() {
        return {
            personal_checked: true,
            security_checked: false,
            membership_checked: false,
        }
    },
    computed: {
        user_data() { return this.$store.getters.user_data }
    },
    methods: {
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
    },
}
</script>