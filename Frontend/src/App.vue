<template>
  <div>
    <Navbar v-if="showLayout" />
    <router-view />
    <Footer v-if="showLayout" />
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { computed } from "vue";
import { useRoute } from "vue-router";
import Navbar from "./components/Navbar.vue";
import Footer from "./components/Footer.vue";
import AOS from "aos";
import "aos/dist/aos.css";

const route = useRoute();
const showLayout = computed(() => !route.meta.hideLayout);

onMounted(() => {
  AOS.init({
    duration: 800,
    easing: "ease-in-out",
    once: true,
    offset: 100,
  });
});
</script>
