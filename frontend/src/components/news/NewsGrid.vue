<template>
  <div>
    <!-- 响应式网格布局容器 -->
    <div 
      ref="gridContainer"
      class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
    >
      <div
        v-for="(news, index) in displayedNews" 
        :key="news.id"
        class="animate-fadeInUp"
        :style="{ animationDelay: `${index * 100}ms` }"
      >
        <NewsCard 
          :news="news"
          @click="handleCardClick(news)"
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
      
      <div v-else-if="hasMoreToShow" class="space-y-4">
        <button 
          @click="loadMore"
          class="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg transition-colors hover:shadow-lg transform hover:scale-105 transition-all duration-200"
        >
          更多
        </button>
        <p class="text-sm text-gray-500 mt-2">
          显示 {{ displayedNews.length }} / {{ newsList.length }} 条新闻
        </p>
      </div>
      
      <div v-else class="text-gray-500">
        <p>已经到底了~</p>
      </div>
    </div>


  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
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

// 显示的新闻数量控制
const displayCount = ref(6) // 默认显示2行（PC端6条，移动端2条）

// 计算显示的新闻列表
const displayedNews = computed(() => {
  return props.newsList.slice(0, displayCount.value)
})

// 处理卡片点击事件
const handleCardClick = (news) => {
  // 这里可以添加跳转到新闻详情页的逻辑
  console.log('点击新闻:', news)
}

// 加载更多新闻
const loadMore = () => {
  const increment = window.innerWidth >= 1024 ? 3 : window.innerWidth >= 768 ? 2 : 1
  displayCount.value += increment
  
  // 如果显示的新闻数量接近总数，触发加载更多数据
  if (displayCount.value >= props.newsList.length - 3 && props.hasMore) {
    emit('load-more')
  }
}

// 检查是否还有更多可显示的新闻
const hasMoreToShow = computed(() => {
  return displayCount.value < props.newsList.length || props.hasMore
})

onMounted(() => {
  // 根据屏幕尺寸设置初始显示数量
  const getInitialCount = () => {
    if (window.innerWidth >= 1024) return 6 // PC端：2行 × 3列
    if (window.innerWidth >= 768) return 4   // 平板：2行 × 2列
    return 2 // 移动端：2行 × 1列
  }
  displayCount.value = getInitialCount()
})
</script>