<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 顶部导航 -->
    <nav class="bg-white shadow-sm border-b">
      <div class="container mx-auto px-4 py-4">
        <div class="flex justify-between items-center">
          <div class="flex items-center space-x-4">
            <router-link 
              to="/admin/dashboard"
              class="text-gray-600 hover:text-gray-900"
            >
              ← 返回管理后台
            </router-link>
            <h1 class="text-2xl font-bold text-gray-900">创建新闻</h1>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主要内容 -->
    <div class="container mx-auto px-4 py-8">
      <div class="max-w-4xl mx-auto">
        <form @submit.prevent="handleSubmit" class="bg-white rounded-lg shadow p-6">
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
                  <img :src="imagePreview" alt="预览" class="max-w-xs rounded-lg">
                </div>
              </div>
            </div>

            <!-- 错误提示 -->
            <div v-if="error" class="text-red-600 text-sm">
              {{ error }}
            </div>

            <!-- 提交按钮 -->
            <div class="flex justify-end space-x-4">
              <router-link 
                to="/admin/dashboard"
                class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
              >
                取消
              </router-link>
              <button 
                type="submit"
                :disabled="isLoading"
                class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
              >
                {{ isLoading ? '创建中...' : '创建新闻' }}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useNewsStore } from '@/store/news'

const router = useRouter()
const newsStore = useNewsStore()

const isLoading = ref(false)
const error = ref('')
const imagePreview = ref('')

const form = reactive({
  title: '',
  description: '',
  image_url: '',
})

const handleImageUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  if (!file.type.startsWith('image/')) {
    error.value = '请选择图片文件'
    return
  }

  if (file.size > 5 * 1024 * 1024) {
    error.value = '图片大小不能超过5MB'
    return
  }

  // 创建预览
  const reader = new FileReader()
  reader.onload = (e) => {
    imagePreview.value = e.target.result
  }
  reader.readAsDataURL(file)

  // 这里模拟上传图片，实际项目中应该调用newsService.uploadImage
  form.image_url = URL.createObjectURL(file)
}

const handleSubmit = async () => {
  isLoading.value = true
  error.value = ''

  try {
    const result = await newsStore.createNews(form)
    
    if (result.success) {
      router.push('/admin/dashboard')
    } else {
      error.value = result.error
    }
  } catch (err) {
    error.value = '创建失败，请重试'
  } finally {
    isLoading.value = false
  }
}
</script>