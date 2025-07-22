<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 顶部导航 -->
    <nav class="bg-white shadow-sm border-b">
      <div class="container mx-auto px-4 py-4">
        <div class="flex justify-between items-center">
          <div class="flex items-center space-x-4">
            <router-link 
              to="/"
              @click="handleBackToHome"
              class="flex items-center space-x-2 text-blue-600 hover:text-blue-800 transition-colors"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
              </svg>
              <span>返回首页</span>
            </router-link>
            <h1 class="text-2xl font-bold text-gray-900">管理后台</h1>
          </div>
          <div class="flex items-center space-x-4">
            <router-link 
              to="/admin/news/create"
              class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              创建新闻
            </router-link>
            <button 
              @click="handleLogout"
              class="text-gray-600 hover:text-gray-900"
            >
              退出登录
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主要内容 -->
    <div class="container mx-auto px-4 py-8">
      <!-- 统计卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-lg font-semibold text-gray-900 mb-2">总新闻数</h3>
          <p class="text-3xl font-bold text-blue-600">{{ totalNews }}</p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-lg font-semibold text-gray-900 mb-2">今日发布</h3>
          <p class="text-3xl font-bold text-green-600">{{ todayNews }}</p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-lg font-semibold text-gray-900 mb-2">总浏览量</h3>
          <p class="text-3xl font-bold text-purple-600">{{ totalViews }}</p>
        </div>
      </div>

      <!-- 新闻列表 -->
      <div class="bg-white rounded-lg shadow">
        <div class="p-6 border-b">
          <h2 class="text-xl font-semibold text-gray-900">新闻管理</h2>
        </div>
        
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b">
                <th class="text-left p-4 font-medium text-gray-700">标题</th>
                <th class="text-left p-4 font-medium text-gray-700">分类</th>
                <th class="text-left p-4 font-medium text-gray-700">创建者</th>
                <th class="text-left p-4 font-medium text-gray-700">发布时间</th>
                <th class="text-left p-4 font-medium text-gray-700">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="news in newsList" :key="news.id" class="border-b hover:bg-gray-50">
                <td class="p-4">
                  <div class="max-w-xs">
                    <p class="font-medium text-gray-900 truncate">{{ news.title }}</p>
                  </div>
                </td>
                <td class="p-4">
                  <span class="px-2 py-1 bg-blue-100 text-blue-800 text-sm rounded">
                    {{ news.category }}
                  </span>
                </td>
                <td class="p-4 text-gray-600">{{ news.creator?.username || 'Unknown' }}</td>
                <td class="p-4 text-gray-600">{{ formatDate(news.created_at) }}</td>
                <td class="p-4">
                  <div class="flex space-x-2">
                    <router-link 
                      :to="`/admin/news/edit/${news.id}`"
                      class="text-blue-600 hover:text-blue-800"
                    >
                      编辑
                    </router-link>
                    <button 
                      @click="handleDelete(news.id)"
                      class="text-red-600 hover:text-red-800"
                      :disabled="isDeleting === news.id"
                    >
                      {{ isDeleting === news.id ? '删除中...' : '删除' }}
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div v-if="isLoading" class="text-center py-8">
          <LoadingSpinner />
        </div>
        
        <div v-if="error" class="text-center py-8">
          <ErrorMessage :message="error" @retry="fetchNews" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { useNewsStore } from '@/store/news'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import ErrorMessage from '@/components/common/ErrorMessage.vue'

const router = useRouter()
const authStore = useAuthStore()
const newsStore = useNewsStore()

const isLoading = ref(false)
const error = ref(null)
const isDeleting = ref(null)

const newsList = computed(() => newsStore.newsList)
const totalNews = computed(() => newsStore.totalNews)

// 计算今日发布的新闻数（模拟数据）
const todayNews = computed(() => {
  const today = new Date().toDateString()
  return newsStore.newsList.filter(news => 
    new Date(news.created_at).toDateString() === today
  ).length
})

// 计算总浏览量（模拟数据）
const totalViews = computed(() => {
  return newsStore.newsList.reduce((sum, news) => sum + (news.views || 0), 0)
})

const fetchNews = async () => {
  isLoading.value = true
  error.value = null
  
  const result = await newsStore.fetchNews(1, 50)
  if (!result.success) {
    error.value = result.error
  }
  isLoading.value = false
}

const handleDelete = async (id) => {
  if (!confirm('确定要删除这条新闻吗？')) return
  
  isDeleting.value = id
  const result = await newsStore.deleteNews(id)
  
  if (!result.success) {
    alert(result.error)
  }
  isDeleting.value = null
}

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}

const handleBackToHome = () => {
  // 设置标记表示从管理后台返回
  sessionStorage.setItem('fromAdmin', 'true')
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

onMounted(() => {
  fetchNews()
})
</script>