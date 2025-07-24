import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './assets/main.css'
import './assets/css/responsive.css' // 引入响应式样式
import { useAuthStore } from './store/auth'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// 应用启动时检查认证状态
const authStore = useAuthStore()
if (authStore.token) {
  authStore.checkAuthStatus()
}

app.mount('#app')