<template>
  <div>
    <!-- 瀑布流布局容器 -->
    <div 
      ref="masonryContainer"
      class="columns-1 md:columns-2 lg:columns-3 xl:columns-4 gap-6 space-y-6"
    >
      <div
        v-for="(news, index) in newsList" 
        :key="news.id"
        class="break-inside-avoid animate-fadeInUp"
        :style="{ animationDelay: `${index * 100}ms` }"
      >
        <NewsCard 
          :news="news"
          @edit="$emit('edit', news)"
          @delete="$emit('delete', news)"
        />
      </div>
    </div>

    <!-- 初始加载状态 -->
    <div v-if="isLoading && newsList.length === 0" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      <p class="mt-4 text-gray-600">正在加载新闻...</p>
    </div>

    <!-- 错误状态 -->
    <div v-if="error && newsList.length === 0" class="text-center py-12">
      <div class="text-red-500 mb-4">
        <svg class="mx-auto h-12 w-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
      </div>
      <p class="text-gray-600 mb-4">加载失败: {{ error }}</p>
      <button 
        @click="$emit('retry')"
        class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition-colors"
      >
        重试
      </button>
    </div>

    <!-- 加载更多区域 -->
    <div v-if="newsList.length > 0" class="text-center py-8">
      <div v-if="isLoading && newsList.length > 0" class="inline-block">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
        <p class="mt-2 text-gray-600">加载更多...</p>
      </div>
      
      <div v-else-if="hasMore" class="space-y-4">
        <button 
          @click="$emit('load-more')"
          class="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg transition-colors"
        >
          加载更多
        </button>
      </div>
      
      <div v-else class="text-gray-500">
        <p>已经到底了~</p>
      </div>
    </div>


  </div>
</template>

<script setup>
import NewsCard from './NewsCard.vue'

const props = defineProps({
  newsList: {
    type: Array,
    required: true
  },
  isLoading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: null
  },
  hasMore: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['load-more', 'retry'])
</script>