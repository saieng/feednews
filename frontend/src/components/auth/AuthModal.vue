<template>
  <Teleport to="body">
    <div 
      v-if="isOpen"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="close"
    >
      <div class="bg-white rounded-lg max-w-md w-full p-6 animate-fadeIn">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-2xl font-bold text-gray-900">
            {{ isLoginMode ? '登录' : '注册' }}
          </h2>
          <button 
            @click="close"
            class="text-gray-400 hover:text-gray-600"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <form @submit.prevent="handleSubmit">
          <div class="space-y-4">
            <div v-if="!isLoginMode">
              <label class="block text-sm font-medium text-gray-700 mb-1">用户名</label>
              <input 
                v-model="form.username"
                type="text"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="请输入用户名"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">邮箱</label>
              <input 
                v-model="form.email"
                type="email"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="请输入邮箱"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">密码</label>
              <input 
                v-model="form.password"
                type="password"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="请输入密码"
              >
            </div>
            
            <div v-if="error" class="text-red-600 text-sm">
              {{ error }}
            </div>
          </div>
          
          <button 
            type="submit"
            :disabled="isLoading"
            class="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors mt-6"
          >
            {{ isLoading ? '处理中...' : (isLoginMode ? '登录' : '注册') }}
          </button>
        </form>
        
        <div class="text-center mt-4">
          <button 
            @click="toggleMode"
            class="text-blue-600 hover:text-blue-800 text-sm"
          >
            {{ isLoginMode ? '没有账号？立即注册' : '已有账号？立即登录' }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { useAuthStore } from '@/store/auth'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['close', 'success'])

const authStore = useAuthStore()

const isLoginMode = ref(true)
const isLoading = ref(false)
const error = ref('')

const form = reactive({
  username: '',
  email: '',
  password: '',
})

const resetForm = () => {
  form.username = ''
  form.email = ''
  form.password = ''
  error.value = ''
}

const toggleMode = () => {
  isLoginMode.value = !isLoginMode.value
  resetForm()
}

const handleSubmit = async () => {
  isLoading.value = true
  error.value = ''
  
  try {
    const result = isLoginMode.value 
      ? await authStore.login({ email: form.email, password: form.password })
      : await authStore.register({ username: form.username, email: form.email, password: form.password })
    
    if (result.success) {
      emit('success')
      close()
    } else {
      error.value = result.error
    }
  } catch (err) {
    error.value = '操作失败，请重试'
  } finally {
    isLoading.value = false
  }
}

const close = () => {
  resetForm()
  emit('close')
}

// 监听模态框关闭，重置表单
watch(() => props.isOpen, (newVal) => {
  if (!newVal) {
    resetForm()
  }
})
</script>