import { defineStore } from 'pinia'
import { authService } from '@/services/authService'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null,
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
  },

  actions: {
    async login(credentials) {
      try {
        const response = await authService.login(credentials)
        this.token = response.data.access_token
        // 从token中解析用户信息或设置基本用户信息
        this.user = {
          email: credentials.email,
          username: credentials.email.split('@')[0] // 临时从邮箱提取用户名
        }
        
        localStorage.setItem('token', this.token)
        localStorage.setItem('user', JSON.stringify(this.user))
        
        return { success: true }
      } catch (error) {
        return { 
          success: false, 
          error: error.response?.data?.detail || '登录失败' 
        }
      }
    },

    async register(userInfo) {
      try {
        const response = await authService.register(userInfo)
        // 注册成功后，设置用户信息
        this.user = {
          username: userInfo.username,
          email: userInfo.email
        }
        
        localStorage.setItem('user', JSON.stringify(this.user))
        
        return { success: true }
      } catch (error) {
        return { 
          success: false, 
          error: error.response?.data?.detail || '注册失败' 
        }
      }
    },

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    },

    async checkAuthStatus() {
      if (this.token) {
        try {
          const response = await authService.getProfile()
          this.user = response.data.user
          return true
        } catch (error) {
          this.logout()
          return false
        }
      }
      return false
    },
  },
})