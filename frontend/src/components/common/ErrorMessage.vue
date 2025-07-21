<template>
  <div class="text-center py-8">
    <div class="text-red-600 mb-4">
      <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
    </div>
    <h3 class="text-lg font-medium text-gray-900 mb-2">{{ title || '出错了' }}</h3>
    <p class="text-gray-600 mb-4">{{ message || '请稍后重试' }}</p>
    <button 
      @click="$emit('retry')"
      class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
    >
      重试
    </button>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  message: String,
})

defineEmits(['retry'])
</script>