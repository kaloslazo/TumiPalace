<template>
    <!-- Error form -->
    <div class="mt-5 bg-red-alert-bg border-t-4 border-red-alert-darker w-full max-w-sm flex flex-row py-3 px-3 z-10 items-center" v-if="error">
        <img class="h-10 w-auto" src="@/assets/svg/error.svg" alt="error-icon">
        <div class="flex flex-col ml-5">
            <h4 class="text-red-alert-darker font-medium text-base">Error</h4>
            <p class="text-red-alert-darker text-xs">{{ error }}</p>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        error: {
            type: String,
            required: true
        }
    },
}

</script>