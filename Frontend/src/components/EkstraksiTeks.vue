<template>
  <section class="py-16 px-6 md:px-16 bg-white">
    <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-10">
      
      <!-- =======================
           BAGIAN KIRI – UPLOAD
      ======================== -->
      <div class="p-6 rounded-2xl border border-gray-200 bg-white">
        <div
          class="border-2 border-dashed border-gray-300 rounded-xl flex flex-col items-center justify-center h-72"
        >
          <Camera class="w-14 h-14 text-gray-700 mb-4" />

          <label
            class="cursor-pointer bg-white border border-gray-300 text-gray-700 text-sm px-4 py-1 rounded-lg hover:bg-gray-100 transition"
          >
            Pilih File Gambar
            <input type="file" accept="image/*" class="hidden" @change="onFileChange" />
          </label>

          <p v-if="selectedFile" class="mt-3 text-sm text-gray-500">
            {{ selectedFile.name }}
          </p>
        </div>

        <button
          class="mt-6 w-full bg-blue-500 hover:bg-blue-600 transition text-white font-medium py-2.5 rounded-xl"
          @click="handleExtract"
          :disabled="loading"
        >
          {{ loading ? 'Memproses...' : 'Ekstrak Sekarang' }}
        </button>
      </div>

      <!-- =======================
           BAGIAN KANAN – HASIL
      ======================== -->
      <div class="p-6 rounded-2xl border border-gray-200 bg-white">
        <h2 class="text-xl font-semibold text-gray-800">Hasil Transkrip</h2>
        <p class="text-gray-500 text-sm mt-1">
          Pastikan foto terlihat jelas untuk hasil ekstrak yang optimal.
        </p>

        <textarea
          v-model="resultText"
          class="mt-4 w-full h-72 border rounded-lg p-3 text-sm text-gray-700 outline-none"
          placeholder="Hasil ekstrak akan muncul di sini..."
        ></textarea>

        <div class="flex flex-col md:flex-row gap-3 mt-4">
          <button
            class="bg-blue-500 hover:bg-blue-600 transition text-white px-6 py-2 rounded-xl"
            @click="handleGrammar"
            :disabled="!resultText"
          >
            Cek Grammar
          </button>

          <button
            class="bg-blue-500 hover:bg-blue-600 transition text-white px-6 py-2 rounded-xl"
            @click="handleSummarize"
            :disabled="!resultText"
          >
            Summarize
          </button>

          <button
            class="bg-green-500 hover:bg-green-600 transition text-white px-6 py-2 rounded-xl"
            @click="handleDownload"
            :disabled="!resultText"
          >
            Unduh PDF
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { Camera } from "lucide-vue-next";

const selectedFile = ref(null);
const resultText = ref("");
const loading = ref(false);

const onFileChange = (e) => {
  selectedFile.value = e.target.files[0];
};

const handleExtract = async () => {
  if (!selectedFile.value) {
    alert("Pilih file gambar terlebih dahulu!");
    return;
  }

  loading.value = true;
  const formData = new FormData();
  formData.append("file", selectedFile.value);

  try {
    const res = await axios.post("http://127.0.0.1:8000/ocr", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    resultText.value = res.data.text;
  } catch (err) {
    console.error(err);
    alert("Gagal mengekstrak teks");
  } finally {
    loading.value = false;
  }
};

const handleGrammar = async () => {
  if (!resultText.value) return;

  try {
    const res = await axios.post("http://127.0.0.1:8000/grammar", new URLSearchParams({ text: resultText.value }));
    resultText.value = res.data.corrected_text;
  } catch (err) {
    console.error(err);
    alert("Gagal memeriksa grammar");
  }
};

const handleSummarize = async () => {
  if (!resultText.value) return;

  try {
    const res = await axios.post("http://127.0.0.1:8000/summarize", new URLSearchParams({ text: resultText.value }));
    resultText.value = res.data.summary;
  } catch (err) {
    console.error(err);
    alert("Gagal membuat ringkasan");
  }
};

const handleDownload = () => {
  const blob = new Blob([resultText.value], { type: "text/plain;charset=utf-8" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "hasil_noteboard.txt";
  link.click();
};
</script>
