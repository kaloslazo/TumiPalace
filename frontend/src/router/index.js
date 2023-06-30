import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";

import store from '@/store/store'

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
    meta: {
      title: 'Claim your welcome bonus',
    },
  },
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/LoginView.vue"),
    meta: {
      title: 'Login',
      hideNavigation: true,
    }
  },
  {
    path: "/register",
    name: "register",
    component: () => import("@/views/RegisterView.vue"),
    meta: {
      title: 'Register',
      hideNavigation: true,
    }
  },
  {
    path: "/profile",
    name: "profile",
    component: () => import("@/views/ProfileView.vue"),
    meta: {
      title: 'Profile',
      requiresAuth: true,
    },
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: () => import("@/views/DashboardView.vue"),
    meta: {
      title: "Avaliable Games",
      requiresAuth: true
    },
  },
  {
    path: "/support",
    name: "support",
    component: () => import("@/views/SupportView.vue"),
    meta: {
      title: 'Support',
      requiresAuth: true,
    },
  },
  {
    path: "/store",
    name: "store",
    component: () => import("@/views/StoreView.vue"),
    meta: {
      title: 'Store',
      requiresAuth: true
    }
  },
  {
    path: "/notauthorized",
    name: "notauthorized",
    component: () => import("@/views/NotAuthorizedView.vue"),
    meta: {
      title: 'Not Authorized',
    }
  },
  {
    path: "/reset_password",
    name: "reset_password_request",
    component: () => import("@/views/RequestResetPasswordView.vue"),
    meta: {
      title: 'Solicitud de restablecimiento de contraseña.',
      hideNavigation: true,
      requiresAuth: false
    },
  },
  {
    path: "/reset_password/:token",
    name: "reset_password",
    component: () => import("@/views/FormResetPasswordView.vue"),
    meta: {
      title: 'Restablecer contraseña',
      hideNavigation: true,
    },
  },
  /*=== GAMES ===*/ 
  {
    path: "/games/slots",
    name: "slots",
    component: () => import("@/views/games/SlotsView.vue"),
    meta: {
      title: 'Slots',
      requiresAuth: true,
    },
  },
  {
    path: "/games/roulette",
    name: "roulette",
    component: () => import("@/views/games/RouletteView.vue"),
    meta: {
      title: 'Roulette',
      requiresAuth: true,
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// check if user is loggedin
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.getters.isLoggedIn) {
      next({ name: 'notauthorized' })
    } else {
      next()
    }
  }
  else {
    next()
  }
})


export default router;