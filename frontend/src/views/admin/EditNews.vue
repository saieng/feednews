<template>
  <div class="min-h-screen bg-gray-50 overflow-y-auto max-h-screen">
    <!-- 返回首页按钮 -->
    <div class="bg-white shadow-sm border-b">
      <div class="container mx-auto px-4 py-4">
        <div class="flex justify-between items-center">
          <h1 class="text-xl sm:text-2xl font-bold text-gray-900">编辑新闻</h1>
          <router-link 
              to="/admin/dashboard"
              class="flex items-center space-x-2 text-blue-600 hover:text-blue-800 transition-colors"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
              </svg>
              <span>返回</span>
            </router-link>
        </div>
      </div>
    </div>

    <!-- 主要内容 -->
    <div class="container mx-auto px-4 py-8">
      <div v-if="isLoading" class="text-center py-8">
        <LoadingSpinner />
      </div>

      <div v-else-if="error" class="text-center py-8">
        <ErrorMessage :message="error" @retry="loadNews" />
      </div>

      <div v-else-if="news" class="max-w-4xl mx-auto">
        <form @submit.prevent="handleSubmit" class="bg-white rounded-lg shadow p-4 sm:p-6">
          <div class="space-y-6">
            <!-- 标题 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">标题 *</label>
              <input 
                v-model="form.title"
                type="text"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="请输入新闻标题"
              >
            </div>

            <!-- 描述 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">描述 *</label>
              <textarea 
                v-model="form.description"
                required
                rows="5"
                maxlength="500"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="请输入新闻描述（最多500字符）"
              ></textarea>
              <div class="text-sm text-gray-500 mt-1">
                {{ form.description.length }}/500 字符
              </div>
            </div>

            <!-- 图片上传 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">封面图片</label>
              <div class="space-y-2">
                <input 
                  type="file"
                  accept="image/*"
                  @change="handleImageUpload"
                  class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                >
                <div v-if="imagePreview" class="mt-2">
                  <img :src="imagePreview" alt="预览" class="max-w-xs max-h-48 object-cover rounded-lg">
                </div>
                <div v-else-if="form.image_url" class="mt-2">
                  <img :src="form.image_url" alt="当前图片" class="max-w-xs max-h-48 object-cover rounded-lg">
                </div>
              </div>
            </div>

            <!-- 错误提示 -->
            <div v-if="submitError" class="text-red-600 text-sm">
              {{ submitError }}
            </div>

            <!-- 提交按钮 -->
            <div class="flex flex-col sm:flex-row justify-end space-y-2 sm:space-y-0 sm:space-x-4">
              <router-link 
                to="/admin/dashboard"
                class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors text-center"
              >
                取消
              </router-link>
              <button 
                type="submit"
                :disabled="isLoading"
                class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
              >
                {{ isLoading ? '更新中...' : '更新新闻' }}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useNewsStore } from '@/store/news'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import ErrorMessage from '@/components/common/ErrorMessage.vue'

const router = useRouter()
const route = useRoute()
const newsStore = useNewsStore()

const news = ref(null)
const isLoading = ref(true)
const error = ref('')
const submitError = ref('')
const isUpdating = ref(false)
const imagePreview = ref('')

const form = reactive({
  title: '',
  description: '',
  image_url: '',
})

const loadNews = async () => {
  isLoading.value = true
  error.value = ''
  
  const result = await newsStore.getNewsById(route.params.id)
  
  if (result.success) {
    news.value = result.data
    Object.assign(form, result.data)
  } else {
    error.value = result.error
  }
  
  isLoading.value = false
}

const handleImageUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  if (!file.type.startsWith('image/')) {
    submitError.value = '请选择图片文件'
    return
  }

  if (file.size > 500 * 1024) { // 限制为500KB
    submitError.value = '图片大小不能超过500KB，请选择更小的图片或压缩后上传'
    return
  }

  // 创建预览和保存图片URL
  const reader = new FileReader()
  reader.onload = (e) => {
    imagePreview.value = e.target.result
    // 使用base64数据作为图片URL，这样保存后也能正常显示
    form.image_url = e.target.result
  }
  reader.readAsDataURL(file)
}

const handleSubmit = async () => {
  isUpdating.value = true
  submitError.value = ''

  try {
    const result = await newsStore.updateNews(route.params.id, form)
    
    if (result.success) {
      router.push('/admin/dashboard')
    } else {
      submitError.value = result.error
    }
  } catch (err) {
    submitError.value = '更新失败，请重试'
  } finally {
    isUpdating.value = false
  }
}



onMounted(() => {
  loadNews()
})
</script>