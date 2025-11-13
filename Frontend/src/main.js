import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import './style.css'
import App from './App.vue'

import Home from './View/Home.vue'
import Ekstraksiteks from './View/Ekstraksiteks.vue'

const routes = [
  { path: '/', component: Home },
  { 
    path: '/ekstraksi-teks',
    component: Ekstraksiteks,
    meta: { hideLayout: true }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
})

createApp(App).use(router).mount('#app')
