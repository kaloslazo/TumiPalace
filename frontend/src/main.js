import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

import "@/utils/axios"
import store from "@/store/store"
import "@/assets/css/tailwind.css"

createApp(App).use(store).use(router).mount("#app");