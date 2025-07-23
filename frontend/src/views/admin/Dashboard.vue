<template>
  <div class="h-screen bg-gray-50 overflow-y-auto">
    <!-- 顶部导航 -->
    <nav class="bg-white shadow-sm border-b sticky top-0 z-10">
      <div class="container mx-auto px-4 py-4">
        <div class="flex justify-between items-center">
          <div class="flex items-center space-x-2 md:space-x-4">
            <router-link to="/" @click="handleBackToHome"
              class="flex items-center space-x-1 md:space-x-2 text-blue-600 hover:text-blue-800 transition-colors">
              <svg class="w-4 h-4 md:w-5 md:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18">
                </path>
              </svg>
              <span class="text-sm md:text-base">返回首页</span>
            </router-link>
            <h1 class="text-lg md:text-2xl font-bold text-gray-900">管理后台</h1>
          </div>
          <div class="flex items-center space-x-2 md:space-x-4">
            <router-link to="/admin/news/create"
              class="bg-blue-600 text-white px-2 py-1 md:px-4 md:py-2 text-sm md:text-base rounded-lg hover:bg-blue-700 transition-colors">
              <span class="hidden md:inline">创建新闻</span>
              <span class="md:hidden">创建</span>
            </router-link>
            <button @click="handleLogout" class="text-gray-600 hover:text-gray-900 text-sm md:text-base">
              <span class="hidden md:inline">退出登录</span>
              <span class="md:hidden">退出</span>
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主要内容 -->
    <div class="container mx-auto px-4 py-8">
      <!-- 统计卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-6 mb-6 md:mb-8">
        <div class="bg-white p-4 md:p-6 rounded-lg shadow">
          <h3 class="text-base md:text-lg font-semibold text-gray-900 mb-2">总新闻数</h3>
          <p class="text-2xl md:text-3xl font-bold text-blue-600">{{ totalNews }}</p>
        </div>
        <div class="bg-white p-4 md:p-6 rounded-lg shadow">
          <h3 class="text-base md:text-lg font-semibold text-gray-900 mb-2">今日发布</h3>
          <p class="text-2xl md:text-3xl font-bold text-green-600">{{ todayNews }}</p>
        </div>
        <div class="bg-white p-4 md:p-6 rounded-lg shadow">
          <h3 class="text-base md:text-lg font-semibold text-gray-900 mb-2">总浏览量</h3>
          <p class="text-2xl md:text-3xl font-bold text-purple-600">{{ totalViews }}</p>
        </div>
      </div>

      <!-- 新闻列表 -->
      <div class="bg-white rounded-lg shadow">
        <div class="p-4 md:p-6 border-b">
          <h2 class="text-lg md:text-xl font-semibold text-gray-900">新闻管理</h2>
        </div>

        <!-- 桌面端表格 -->
        <div class="hidden md:block overflow-x-auto">
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
                <td class="p-4 text-gray-600">{{ news.creator_username || 'Unknown' }}</td>
                <td class="p-4 text-gray-600">{{ formatDate(news.created_at) }}</td>
                <td class="p-4">
                  <div class="flex space-x-2">
                    <router-link :to="`/admin/news/edit/${news.id}`" class="text-blue-600 hover:text-blue-800">
                      编辑
                    </router-link>
                    <button @click="handleDelete(news.id)" class="text-red-600 hover:text-red-800"
                      :disabled="isDeleting === news.id">
                      {{ isDeleting === news.id ? '删除中...' : '删除' }}
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 手机端卡片布局 -->
        <div class="md:hidden">
          <div v-for="news in newsList" :key="news.id" class="border-b p-4 hover:bg-gray-50">
            <div class="space-y-2">
              <div class="flex justify-between items-start">
                <h3 class="font-medium text-gray-900 text-sm leading-tight flex-1 mr-2">{{ news.title }}</h3>
                <span class="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded whitespace-nowrap">
                  {{ news.category }}
                </span>
              </div>
              <div class="text-xs text-gray-600">
                <p>创建者: {{ news.creator_username || 'Unknown' }}</p>
                <p>时间: {{ formatDate(news.created_at) }}</p>
              </div>
              <div class="flex space-x-3 pt-2">
                <router-link :to="`/admin/news/edit/${news.id}`" class="text-blue-600 hover:text-blue-800 text-sm">
                  编辑
                </router-link>
                <button @click="handleDelete(news.id)" class="text-red-600 hover:text-red-800 text-sm"
                  :disabled="isDeleting === news.id">
                  {{ isDeleting === news.id ? '删除中...' : '删除' }}
                </button>
              </div>
            </div>
          </div>
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