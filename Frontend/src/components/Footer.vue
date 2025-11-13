<template>
  <footer 
    class="bg-gray-900 text-gray-300 py-14 px-6 md:px-12"
    data-aos="fade-up"
    data-aos-duration="700"
  >
    <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-10">

      <!-- Logo & Deskripsi -->
      <div class="space-y-4">
        <div class="flex items-center gap-3">
          <img :src="logo" alt="NoteBoard AI" class="w-10 h-10" />
          <h2 class="text-lg font-semibold text-white">NoteBoard AI</h2>
        </div>

        <p class="text-sm leading-relaxed text-gray-400">
          Ubah foto catatan, buku, atau tulisan tangan menjadi teks digital yang rapi dan siap dipakai.
        </p>
      </div>

      <!-- Navigasi -->
      <div>
        <h3 class="text-white font-semibold mb-4">Menu</h3>
        <ul class="space-y-3 text-sm">
          <li><a href="#home" class="hover:text-white transition">Beranda</a></li>
          <li><a href="#fitur" class="hover:text-white transition">Fitur</a></li>
          <li><a href="#cara-kerja" class="hover:text-white transition">Cara Kerja</a></li>
          <li><a href="#pricing" class="hover:text-white transition">Harga</a></li>
        </ul>
      </div>

      <!-- Social Media -->
      <div>
        <h3 class="text-white font-semibold mb-4">Social Media</h3>

        <div class="flex items-center gap-4">
          <a href="#" class="hover:text-white transition">
            <Instagram class="w-5 h-5" />
          </a>
          <a href="#" class="hover:text-white transition">
            <Github class="w-5 h-5" />
          </a>
          <a href="#" class="hover:text-white transition">
            <Youtube class="w-5 h-5" />
          </a>
        </div>
      </div>

      <!-- Copyright -->
      <div class="flex md:items-end">
        <p class="text-sm text-gray-400">
          © 2025 NoteBoard AI. All rights reserved.
        </p>
      </div>

    </div>
  </footer>
</template>

<script setup>
import { Instagram, Github, Youtube } from "lucide-vue-next";
import logo from '../assets/Logo-Note-Board.png'
</script>
