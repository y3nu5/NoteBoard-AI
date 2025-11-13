<template>
  <header class="bg-white shadow-sm">
    <div class="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <img :src="logo" alt="Logo" class="w-15 h-15 object-contain" />
        <div>
          <p class="font-bold text-lg font-poppins">
            <span class="text-blue-500">NoteBoard.</span
            ><span class="text-primary">AI</span>
          </p>
        </div>
      </div>

      <!-- desktop menu -->
      <nav class="hidden md:flex items-center gap-6">
        <a href="#home" class="hover:text-blue-500" data-aos="fade-down"
          >Beranda</a
        >
        <a
          href="#features"
          class="hover:text-blue-500"
          data-aos="fade-down"
          data-aos-delay="50"
          >Fitur</a
        >
        <router-link
          to="/ekstraksi-teks"
          class="hover:text-blue-500"
          data-aos="fade-down"
          data-aos-delay="100"
        >
          Mulai Coba
        </router-link>
      </nav>

      <!-- mobile hamburger -->
      <div class="md:hidden">
        <button
          @click="toggle"
          :aria-expanded="open"
          aria-label="Toggle menu"
          class="p-2 rounded-md focus:outline-none focus:ring"
        >
          <component :is="open ? X : Menu" class="w-6 h-6" />
        </button>
      </div>
    </div>

    <!-- mobile panel -->
    <transition name="slide-fade">
      <div v-if="open" class="md:hidden bg-white border-t">
        <div class="px-4 py-4 flex flex-col gap-3">
          <a @click="close" href="#home" class="block">Beranda</a>
          <a @click="close" href="#features" class="block">Fitur</a>
          <a @click="close" href="#try" class="block btn-primary"
            >Mulai Coba</a
          >
        </div>
      </div>
    </transition>
  </header>
</template>

<script setup>
import { ref } from "vue";
import { Menu, X } from "lucide-vue-next";
import logo from "../assets/Logo-Note-Board.png";

const open = ref(false);
const toggle = () => (open.value = !open.value);
const close = () => (open.value = false);
</script>

<style scoped>
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.25s ease;
}
.slide-fade-enter-from {
  transform: translateY(-6px);
  opacity: 0;
}
.slide-fade-enter-to {
  transform: translateY(0);
  opacity: 1;
}
</style>
