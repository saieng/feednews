<template>
  <article class="relative group [perspective:1000px] h-[400px]">
    <!-- 3D卡片容器 -->
    <div 
      class="relative w-full h-full transition-all duration-700 [transform-style:preserve-3d] group-hover:[transform:rotateY(180deg)]"
    >
      <!-- 卡片正面 -->
      <div class="absolute inset-0 [backface-visibility:hidden]">
        <!-- 渐变边框容器 -->
        <div class="relative w-full h-full p-0.5 bg-gradient-to-br from-purple-500 via-pink-500 to-blue-500 rounded-2xl">
          <div class="w-full h-full bg-white rounded-2xl overflow-hidden">
            <!-- 图片容器 -->
            <div class="relative h-48 overflow-hidden">
              <!-- 加载占位符 -->
              <div 
                v-if="imageLoading"
                class="absolute inset-0 bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 animate-pulse"
              ></div>
              
              <!-- 新闻图片 -->
              <img 
                :src="news.image || '/api/placeholder/400/300'"
                :alt="news.title"
                class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                @load="handleImageLoad"
                @error="handleImageError"
              />
              
              <!-- 图片悬停遮罩 -->
              <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                <div class="absolute bottom-4 left-4 text-white">
                  <span class="text-sm font-medium">{{ news.category || '新闻' }}</span>
                </div>
              </div>
            </div>
            
            <!-- 内容区域 -->
            <div class="p-6">
              <h3 class="text-xl font-bold text-gray-900 mb-2 line-clamp-2 group-hover:text-blue-600 transition-colors">
                {{ news.title }}
              </h3>
              
              <p class="text-gray-600 text-sm mb-4 line-clamp-3">
                {{ news.description || news.content?.substring(0, 100) + '...' }}
              </p>
              
              <div class="flex items-center justify-between text-sm text-gray-500">
                <span>{{ formatDate(news.publishedAt || news.createdAt) }}</span>
                <span class="text-blue-600 font-medium group-hover:text-blue-700">阅读更多 →</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 卡片背面 -->
      <div class="absolute inset-0 [backface-visibility:hidden] [transform:rotateY(180deg)]">
        <div class="relative w-full h-full p-0.5 bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 rounded-2xl">
          <div class="w-full h-full bg-gray-900 rounded-2xl p-6 flex flex-col justify-between">
            <div>
              <h4 class="text-white font-bold text-lg mb-3">详细信息</h4>
              <div class="space-y-2 text-sm text-gray-300">
                <p><span class="font-medium">作者:</span> {{ news.author || '未知' }}</p>
                <p><span class="font-medium">来源:</span> {{ news.source || 'FeedNews' }}</p>
                <p><span class="font-medium">发布时间:</span> {{ formatDate(news.publishedAt || news.createdAt) }}</p>
              </div>
            </div>
            
            <div class="flex space-x-3">
              <button 
                @click="$emit('edit', news)"
                class="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg transition-colors"
              >
                编辑
              </button>
              <button 
                @click="$emit('delete', news)"
                class="flex-1 bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-lg transition-colors"
              >
                删除
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 悬停发光效果 -->
    <div class="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300">
      <div class="absolute inset-0 bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 rounded-2xl blur-xl opacity-50"></div>
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

const emit = defineEmits(['edit', 'delete'])

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