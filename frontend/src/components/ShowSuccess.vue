<template>
    <!-- Error form -->
    <div class="mt-5 bg-green-200 border-t-4 border-green-700 w-full max-w-sm flex flex-row py-3 px-3 z-10 items-center" v-if="success">
        <img class="h-10 w-auto" src="@/assets/svg/cloud_ok.svg" alt="error-icon">
        <div class="flex flex-col ml-5">
            <!-- si se recibe title se pone, caso contrario es enhorabuea -->
            <h4 class="text-green-900 font-medium text-base">{{ show_title }}</h4>
            <p class="text-green-900 text-xs">{{  success }}</p>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        success: {
            type: String,
            required: true
        },
        title: {
            type: String,
            required: false
        }
    },
    computed: {
        // si no se recibe title es enhorabue
        show_title() { return this.title ? this.title : 'Enhorabuena' }
    }
}

</script>