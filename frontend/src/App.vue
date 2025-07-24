<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <!-- 导航栏 -->
    <nav v-if="!isAdminPage" class="bg-white shadow-sm border-b">
      <div class="container mx-auto px-4 py-4">
        <div class="flex justify-between items-center">
          <div class="flex items-center space-x-8">
            <!-- <router-link to="/" class="text-xl font-bold text-gray-900">FeedNews</router-link>
            <div class="hidden md:flex space-x-6">
              <router-link to="/" class="text-gray-600 hover:text-gray-900">首页</router-link>
              <router-link 
                v-if="authStore.isAuthenticated" 
                to="/admin/dashboard" 
                class="text-gray-600 hover:text-gray-900"
              >
                管理后台
              </router-link>
          </div> -->
          </div>
          <!-- 
          <div class="flex items-center space-x-4">
            <button v-if="!authStore.isAuthenticated" @click="openAuthModal"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
              登录
            </button>
            <div v-else class="flex items-center space-x-4">
              <span class="text-gray-700">{{ authStore.user?.username || '用户' }}</span>
              <button @click="handleLogout" class="text-gray-600 hover:text-gray-900">
                退出
              </button>
            </div>
        </div> -->
        </div>
      </div>
    </nav>

    <!-- 进度条 -->
    <div v-if="isLoading" class="fixed top-0 left-0 w-full h-1 bg-blue-500 z-50 animate-pulse"></div>

    <!-- 主要内容 -->
    <main>
      <router-view />
    </main>

    <!-- 认证模态框 -->
    <AuthModal :is-open="isAuthModalOpen" @close="closeAuthModal" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import AuthModal from '@/components/auth/AuthModal.vue'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()
const isAuthModalOpen = ref(false)
const isLoading = ref(false)

// 检查是否在管理后台页面
const isAdminPage = computed(() => {
  return route.path.startsWith('/admin')
})

const openAuthModal = () => {
  isAuthModalOpen.value = true
}

const closeAuthModal = () => {
  isAuthModalOpen.value = false
}

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}
</script>