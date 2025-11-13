<template>
  <div
    class="bg-white w-full rounded-3xl p-6 border border-gray-100 shadow-lg transition hover:shadow-xl"
    :data-aos="aos"
    :data-aos-delay="delay"
  >
    <div class="w-10 h-10 flex items-center justify-center rounded-lg bg-blue-100 text-blue-600 mb-4">
      <component :is="icon" class="w-6 h-6" />
    </div>

    <h3 class="font-semibold text-gray-800 mb-2">
      {{ title }}
    </h3>

    <p class="text-sm text-gray-600 leading-relaxed">
      {{ description }}
    </p>
  </div>
</template>

<script setup>
defineProps({
  icon: Object,
  title: String,
  description: String,
  aos: {
    type: String,
    default: "zoom-in"
  },
  delay: {
    type: Number,
    default: 0
  }
});
</script>
