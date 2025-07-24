<template>
  <article
    class="relative group cursor-pointer bg-white rounded-xl overflow-hidden shadow-md hover:shadow-xl transition-all duration-300 hover:-translate-y-2"
    @click="$emit('click', news)">
    <!-- 图片区域 - 16:9 比例 -->
    <div class="relative w-full aspect-video overflow-hidden">
      <!-- 加载占位符 -->
      <div v-if="imageLoading"
        class="absolute inset-0 bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 animate-pulse"></div>

      <!-- 新闻图片 -->
      <img :src="news.image_url || news.image || '/api/placeholder/400/225'" :alt="news.title"
        class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
        @load="handleImageLoad" @error="handleImageError" />

      <!-- 图片悬停遮罩 -->
      <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all duration-300"></div>
    </div>

    <!-- 内容区域 -->
    <div class="p-6">
      <!-- 标题 - 最多2行 -->
      <h3
        class="text-lg font-bold text-gray-900 mb-3 line-clamp-2 group-hover:text-blue-600 transition-colors leading-tight">
        {{ news.title }}
      </h3>

      <!-- 描述 - 最多2行 -->
      <p class="text-gray-600 text-sm mb-4 line-clamp-2 leading-relaxed">
        {{ news.description || news.content?.substring(0, 120) + '...' || '暂无描述' }}
      </p>

      <!-- 底部信息 -->
      <div class="flex items-center justify-between text-sm">
        <!-- 创作者标签 -->
        <span class="text-blue-600 font-medium">
          By: {{ news.creator_username || '未知作者' }}
        </span>

        <!-- 发布时间 -->
        <span class="text-gray-500">
          {{ formatDate(news.created_at || news.publishedAt || news.createdAt) }}
        </span>
      </div>
    </div>
  </article>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  news: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['click'])

const imageLoading = ref(true)

const handleImageLoad = () => {
  imageLoading.value = false
}

const handleImageError = () => {
  imageLoading.value = false
}

const formatDate = (dateString) => {
  if (!dateString) return '未知时间'
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>