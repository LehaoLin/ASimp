import { createRouter, createWebHistory } from "vue-router";

import Home from "@/components/Home.vue";
import Play from "@/components/Play_.vue";
import Topics from "@/components/Topics.vue";

const routes = [
  {
    path: "/",
    component: Home,
  },
  {
    path: "/topics",
    component: Topics,
  },
  {
    path: "/play",
    component: Play,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
