<template>
  <section
    id="home"
    class="mt-8 rounded-lg p-8 md:p-10"
    style="background-color: #eaf1ff"
    data-aos="fade-up"
  >
    <div class="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-10 items-center">

      <!-- LEFT TEXT -->
      <div>
        <h1 class="text-3xl md:text-4xl font-extrabold leading-tight">
          Konversi Catatan Anda <br />
          Dengan <span class="text-primary">NoteBoard AI</span>
        </h1>

        <p class="mt-4 text-gray-600 max-w-md">
          NoteBoard AI adalah platform berbasis web yang mampu mengkonversi
          catatan atau buku anda ke teks digital.
        </p>

        <div class="mt-6 flex flex-wrap gap-4">
          <a
            href="#try"
            class="bg-blue-500 text-white px-5 py-2 rounded-lg shadow hover:bg-blue-400 transition"
            data-aos="fade-right"
          >
            Mulai Sekarang
          </a>

          <a
            href="#features"
            class="border border-gray-300 bg-white px-5 py-2 rounded-lg shadow hover:bg-blue-500 transition"
            data-aos="fade-right"
            data-aos-delay="100"
          >
            Pelajari Lebih Lanjut
          </a>
        </div>
      </div>

      <!-- RIGHT CARD -->
      <div class="flex justify-center md:justify-end">
        <div
          class="bg-white p-6 rounded-2xl shadow-xl w-full max-w-sm"
          data-aos="zoom-in"
          data-aos-delay="150"
        >
          <img
            :src="gambarnulis"
            alt="preview"
            class="w-full h-[200px] object-cover rounded-xl"
          />
          <p class="text-sm text-center mt-4 text-gray-500">
            Unggah foto tulisan tangan/buku, ekstrak teks, dan ekspor ke PDF dengan mudah.
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import gambarnulis from '../assets/gambarnulis.jpeg'
</script>

<style scoped>
/* warna utama */
.text-primary {
  color: #2b7cff;
}
.bg-primary {
  background-color: #2b7cff;
}
</style>
