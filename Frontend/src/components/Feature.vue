<template>
  <section id="features" class="py-16">
    <div class="max-w-6xl mx-auto px-6">

      <!-- Title -->
      <h2 class="text-center text-xl font-semibold text-gray-800 mb-12" data-aos="fade-up">
        Fitur Utama
      </h2>

      <!-- Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">

        <!-- Upload -->
        <Feature_Card
          :icon="Camera"
          title="Unggah atau Ambil Foto"
          description="Unggah foto tulisan tangan di papan tulis atau buku atau catatan langsung dari galeri atau kamera HP."
          aos="zoom-in"
          :delay="0"
        />

        <!-- Ekstraksi Teks -->
        <Feature_Card
          :icon="FileText"
          title="Ekstraksi Teks"
          description="Foto yang sudah diunggah akan di ekstraksi menjadi teks digital."
          aos="zoom-in"
          :delay="100"
        />

        <!-- Koreksi Ejaan -->
        <Feature_Card
          :icon="Wand2"
          title="Koreksi Ejaan dan Summarize Otomatis"
          description="Setelah teks diekstrak, sistem akan memperbaiki ejaan dan tata bahasa."
          aos="zoom-in"
          :delay="200"
        />

        <!-- Editor Teks Manual -->
        <Feature_Card
          :icon="Edit"
          title="Editor Teks Manual"
          description="Pengguna dapat mengedit teks hasil ekstraksi secara manual langsung di halaman editor."
          aos="fade-up"
          :delay="0"
        />

        <!-- Ekspor PDF -->
        <Feature_Card
          :icon="FileDown"
          title="Ekspor Hasil ke PDF"
          description="Setelah selesai, pengguna bisa menyimpan hasil akhir dalam format PDF."
          aos="fade-up"
          :delay="100"
        />

      </div>

    </div>
  </section>
</template>

<script setup>
import Feature_Card from "./Feature_Card.vue";

import {
  Camera,
  FileText,
  Wand2,
  Edit,
  FileDown
} from "lucide-vue-next";
</script>
