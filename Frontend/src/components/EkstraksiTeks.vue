<template>
  <section class="py-16 px-6 md:px-10 bg-white">
    <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-10">

      <!-- LEFT PANEL -->
      <div class="p-6 rounded-2xl border border-gray-200 bg-white">
        <div class="border-2 border-dashed border-gray-300 rounded-xl flex flex-col items-center justify-center h-72">
          <Camera class="w-14 h-14 text-gray-700 mb-4" />

          <!-- Upload -->
          <label
            class="cursor-pointer bg-white border border-gray-300 text-gray-700 text-sm px-4 py-1 rounded-lg hover:bg-gray-100 transition">
            Pilih Foto
            <input type="file" accept="image/*" multiple class="hidden" @change="onFileChange($event)" />
          </label>

          <!-- Camera Button -->
          <button class="mt-4 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition"
            @click="openCamera">
            Gunakan Kamera
          </button>

          <div v-if="selectedFiles.length" class="mt-3 text-sm text-gray-500">
            {{ selectedFiles.length }} file dipilih
          </div>
        </div>

        <!-- Preview -->
        <div v-if="previewImages.length" class="mt-4 grid grid-cols-3 gap-3">
          <div v-for="(img, index) in previewImages" :key="index" class="relative">
            <img :src="img" class="w-full h-24 object-cover rounded-lg border" />
            <button class="absolute top-1 right-1 bg-red-500 text-white rounded-full w-6 h-6 text-xs flex items-center justify-center hover:bg-red-600"
              @click="removeImage(index)">
              ✕
            </button>
          </div>
        </div>

        <!-- Extract Button -->
        <button class="mt-6 w-full bg-blue-500 hover:bg-blue-600 transition text-white font-medium py-2.5 rounded-xl"
          @click="handleExtract" :disabled="loading">
          {{ loading ? "Memproses..." : "Ekstrak Sekarang" }}
        </button>
      </div>

      <!-- RIGHT PANEL -->
      <div class="p-6 rounded-2xl border border-gray-200 bg-white relative">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold text-gray-800">Hasil Transkrip</h2>
          
          <!-- Toggle Edit Mode Button -->
          <button 
            v-if="resultText"
            @click="toggleEditMode"
            class="text-sm px-3 py-1 rounded-lg border transition"
            :class="isEditMode ? 'bg-green-500 text-white border-green-500' : 'bg-gray-100 text-gray-700 border-gray-300 hover:bg-gray-200'">
            {{ isEditMode ? '✓ Mode Edit' : '✏️ Edit' }}
          </button>
        </div>

        <!-- EDITABLE MODE (Plain Text) -->
        <textarea
          v-if="isEditMode"
          v-model="resultText"
          @input="onManualEdit"
          class="mt-4 w-full h-72 border rounded-lg p-3 text-sm text-gray-700 overflow-auto resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Teks hasil ekstraksi akan muncul di sini..."
        ></textarea>

        <!-- VIEW MODE (with Grammar Highlights) -->
        <div
          v-else
          ref="resultContainer"
          class="mt-4 w-full h-72 border rounded-lg p-3 text-sm text-gray-700 overflow-auto whitespace-pre-wrap"
          :class="{ 'bg-gray-50': !resultText }"
          v-html="highlightedHtml || '<span class=\'text-gray-400\'>Teks hasil ekstraksi akan muncul di sini...</span>'"
          @click="onResultClick($event)">
        </div>

        <!-- Popup Grammar Suggestion -->
        <div
          v-if="popup.visible"
          :style="popup.style"
          class="absolute z-50 bg-white border shadow-lg rounded-md p-2 w-64">
          <div class="text-sm font-medium text-gray-700 mb-1">
            {{ popup.message }}
          </div>
          <div class="text-sm">
            Saran:
            <span class="font-semibold text-green-600">{{ popup.suggestion }}</span>
          </div>

          <div class="flex justify-end gap-2 mt-3">
            <button class="px-2 py-1 rounded text-sm border hover:bg-gray-100" @click="closePopup">Tutup</button>
            <button class="px-2 py-1 rounded text-sm bg-green-500 text-white hover:bg-green-600" @click="applySuggestion">Terapkan</button>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex flex-col md:flex-row gap-3 mt-5">
          <button class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-xl disabled:bg-gray-400 disabled:cursor-not-allowed transition"
            :disabled="!resultText || isEditMode" 
            @click="handleGrammar">
            📝 Grammar Check
          </button>

          <button class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-xl disabled:bg-gray-400 disabled:cursor-not-allowed transition"
            :disabled="!resultText" 
            @click="handleSummarize">
            📄 Summarize
          </button>

          <button class="bg-green-500 hover:bg-green-600 text-white px-6 py-2 rounded-xl disabled:bg-gray-400 disabled:cursor-not-allowed transition"
            :disabled="!resultText" 
            @click="handleDownload">
            📥 Download PDF
          </button>
        </div>

        <!-- Info Text -->
        <p v-if="isEditMode" class="text-xs text-gray-500 mt-3">
          💡 Tip: Mode edit aktif. Grammar check tidak tersedia saat mengedit. Klik "✓ Mode Edit" untuk kembali.
        </p>
      </div>
    </div>

    <!-- Camera Modal -->
    <div v-if="cameraActive" class="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-4 w-[90%] max-w-md">
        <video ref="videoRef" autoplay playsinline class="w-full rounded-lg"></video>

        <div class="flex justify-between mt-4">
          <button class="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600 transition" @click="closeCamera">Batal</button>
          <button class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition" @click="capturePhoto">Ambil Foto</button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, reactive, nextTick } from "vue";
import axios from "axios";
import { Camera } from "lucide-vue-next";

// Backend URL - sesuaikan dengan Hugging Face Space Anda
const BASE_URL = import.meta.env.VITE_API_URL || "https://yunus789-noteboard-ai-backend.hf.space";

/* FILE STATE */
const selectedFiles = ref([]);
const previewImages = ref([]);
const resultText = ref("");
const loading = ref(false);

/* EDIT MODE */
const isEditMode = ref(false);

const toggleEditMode = () => {
  if (isEditMode.value) {
    grammarErrors.value = [];
    highlightedHtml.value = escapeHtml(resultText.value);
  }
  isEditMode.value = !isEditMode.value;
  closePopup();
};

const onManualEdit = () => {
  grammarErrors.value = [];
};

/* CAMERA */
const cameraActive = ref(false);
const videoRef = ref(null);
let stream = null;

const openCamera = async () => {
  try {
    cameraActive.value = true;
    stream = await navigator.mediaDevices.getUserMedia({ video: true });
    videoRef.value.srcObject = stream;
  } catch {
    cameraActive.value = false;
    alert("Tidak dapat membuka kamera.");
  }
};

const closeCamera = () => {
  stream?.getTracks()?.forEach((t) => t.stop());
  cameraActive.value = false;
};

const capturePhoto = () => {
  const canvas = document.createElement("canvas");
  const video = videoRef.value;
  canvas.width = video.videoWidth || 640;
  canvas.height = video.videoHeight || 480;

  canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);
  canvas.toBlob((blob) => {
    const file = new File([blob], "camera.jpg", { type: "image/jpeg" });
    selectedFiles.value.push(file);
    previewImages.value.push(URL.createObjectURL(file));
  });

  closeCamera();
};

/* FILE UPLOAD */
const onFileChange = (e) => {
  const files = Array.from(e.target.files);
  files.forEach((file) => {
    selectedFiles.value.push(file);
    previewImages.value.push(URL.createObjectURL(file));
  });
};

const removeImage = (i) => {
  URL.revokeObjectURL(previewImages.value[i]);
  previewImages.value.splice(i, 1);
  selectedFiles.value.splice(i, 1);
};

/* OCR PROCESS */
const handleExtract = async () => {
  if (!selectedFiles.value.length) return alert("Pilih foto terlebih dahulu!");
  loading.value = true;

  const fd = new FormData();
  selectedFiles.value.forEach((f) => fd.append("files", f));

  try {
    const res = await axios.post(`${BASE_URL}/ocr`, fd);
    resultText.value = res.data.results.join("\n\n---\n\n");
    grammarErrors.value = [];
    highlightedHtml.value = escapeHtml(resultText.value);
    isEditMode.value = false;
  } catch (err) {
    console.error(err);
    alert("OCR gagal. Pastikan backend berjalan.");
  }

  loading.value = false;
};

/* GRAMMAR HIGHLIGHT */
const grammarErrors = ref([]);
const highlightedHtml = ref("");
const resultContainer = ref(null);

function escapeHtml(s) {
  if (!s) return "";
  return s
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function generateHighlightedHtml() {
  const text = resultText.value;
  if (!grammarErrors.value.length) {
    highlightedHtml.value = escapeHtml(text);
    return;
  }

  let html = "";
  let last = 0;

  for (const err of grammarErrors.value) {
    html += escapeHtml(text.slice(last, err.start));

    const inner = escapeHtml(text.slice(err.start, err.end));
    html += `<span class="error-span" data-start="${err.start}"
      style="text-decoration: underline red 2px; cursor: pointer;">
      ${inner}</span>`;

    last = err.end;
  }

  html += escapeHtml(text.slice(last));
  highlightedHtml.value = html;
}

/* POPUP */
const popup = reactive({
  visible: false,
  suggestion: "",
  message: "",
  error: null,
  style: { top: "0px", left: "0px", position: "absolute" }
});

function onResultClick(ev) {
  const span = ev.target.closest(".error-span");
  if (!span) return closePopup();

  const start = parseInt(span.dataset.start);
  const err = grammarErrors.value.find((e) => e.start === start);
  if (!err) return;

  const rect = resultContainer.value.getBoundingClientRect();
  popup.style.left = `${ev.clientX - rect.left + 5}px`;
  popup.style.top = `${ev.clientY - rect.top + 5}px`;
  popup.message = err.message;
  popup.suggestion = err.suggestion;
  popup.error = err;
  popup.visible = true;
}

function closePopup() {
  popup.visible = false;
}

/* APPLY SUGGESTION */
function applySuggestion() {
  const err = popup.error;
  if (!err) return;

  resultText.value =
    resultText.value.slice(0, err.start) +
    err.suggestion +
    resultText.value.slice(err.end);

  grammarErrors.value = [];
  highlightedHtml.value = escapeHtml(resultText.value);

  closePopup();
}

/* GRAMMAR API */
const handleGrammar = async () => {
  if (isEditMode.value) {
    alert("Nonaktifkan mode edit terlebih dahulu.");
    return;
  }

  const fd = new FormData();
  fd.append("text", resultText.value);

  try {
    const res = await axios.post(`${BASE_URL}/grammar`, fd);
    resultText.value = res.data.corrected_text;
    grammarErrors.value = res.data.errors.sort((a, b) => a.start - b.start);

    await nextTick();
    generateHighlightedHtml();
  } catch (err) {
    console.error(err);
    alert("Grammar gagal. Pastikan backend berjalan.");
  }
};

/* SUMMARIZE */
const handleSummarize = async () => {
  const fd = new FormData();
  fd.append("text", resultText.value);

  try {
    const res = await axios.post(`${BASE_URL}/summarize`, fd);
    resultText.value = res.data.summary;
    grammarErrors.value = [];
    highlightedHtml.value = escapeHtml(resultText.value);
    isEditMode.value = false;
  } catch (err) {
    console.error(err);
    alert("Summary gagal. Pastikan backend berjalan.");
  }
};

/* PDF */
const handleDownload = async () => {
  const fd = new FormData();
  fd.append("text", resultText.value);

  try {
    const res = await axios.post(`${BASE_URL}/export-pdf`, fd, {
      responseType: "blob"
    });

    const blob = new Blob([res.data], { type: "application/pdf" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "output.pdf";
    a.click();
    URL.revokeObjectURL(url);
  } catch (err) {
    console.error(err);
    alert("Gagal membuat PDF. Pastikan backend berjalan.");
  }
};
</script>

<style scoped>
.error-span {
  text-decoration: underline red 2px;
  cursor: pointer;
}

.error-span:hover {
  background-color: rgba(239, 68, 68, 0.1);
}
</style>