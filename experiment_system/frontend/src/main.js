import { createApp } from "vue";
import { createPinia } from "pinia";

// import "./style.css";

import ElementPlus from "element-plus";

import "element-plus/dist/index.css";
// import "element-plus/theme-chalk/dark/css-vars.css";

import App from "./App.vue";
import router from "@/router";

const app = createApp(App);

const pinia = createPinia();

app.use(pinia);
app.use(router);
app.use(ElementPlus);

app.mount("#app");
