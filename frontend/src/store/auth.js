import { defineStore } from 'pinia'
import { authService } from '@/services/authService'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null,
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
    isAuthenticated: (state) => !!state.token,
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
        
        // 注册成功后自动登录
        const loginResult = await this.login({
          email: userInfo.email,
          password: userInfo.password
        })
        
        if (loginResult.success) {
          return { success: true, message: '注册成功并已自动登录' }
        } else {
          // 注册成功但登录失败，仍然返回成功但提示需要手动登录
          return { 
            success: true, 
            message: '注册成功，请手动登录',
            needManualLogin: true 
          }
        }
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
          // 尝试调用一个需要认证的接口来验证token有效性
          // 这里可以调用任何需要认证的接口，比如获取新闻列表
          const response = await fetch(`${import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8001/api/v1'}/news?page=1&limit=1`, {
            headers: {
              'Authorization': `Bearer ${this.token}`
            }
          })
          
          if (response.ok) {
            return true
          } else {
            this.logout()
            return false
          }
        } catch (error) {
          this.logout()
          return false
        }
      }
      return false
    },
  },
})