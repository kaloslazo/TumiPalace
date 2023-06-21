import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";

import store from '@/store/store'

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/LoginView.vue"),
    meta: {
      title: 'Login',
    }
  },
  {
    path: "/register",
    name: "register",
    component: () => import("@/views/RegisterView.vue"),
    meta: {
      title: 'Register',
    }
  },
  {
    path: "/profile",
    name: "profile",
    component: () => import("@/views/ProfileView.vue"),
    meta: { 
      requiresAuth: true,
      title: 'Profile',
    },
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: () => import("@/views/DashboardView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/support",
    name: "support",
    component: () => import("@/views/SupportView.vue"),
    meta: { 
      requiresAuth: true,
      title: 'Support',
    },
  },
  {
    path: "/store",
    name: "store",
    component: () => import("@/views/StoreView.vue"),
    meta: {
      title: 'Store',
    }
  },
  {
    path: "/notauthorized",
    name: "notauthorized",
    component: () => import("@/views/NotAuthorizedView.vue"),
    meta: {
      title: 'Not Authorized',
    }
  }
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