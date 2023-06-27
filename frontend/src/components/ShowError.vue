<template>
    <div>
        <!-- Error form -->
        <div class="mt-5 bg-red-alert-bg border-t-4 border-red-alert-darker w-full max-w-sm flex flex-row py-3 px-3 z-10 items-center">
            <img class="h-10 w-auto" src="@/assets/svg/error.svg" alt="error-icon">
            <div class="flex flex-col ml-5">
                <h4 class="text-red-alert-darker font-medium text-lg">Error</h4>
                <p class="text-red-alert-darker text-sm">{{ error }}</p>
            </div>
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