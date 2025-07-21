import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000/api'

class AuthService {
  constructor() {
    this.api = axios.create({
      baseURL: `${API_URL}/auth`,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // 请求拦截器添加token
    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('token')
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      (error) => Promise.reject(error)
    )

    // 响应拦截器处理错误
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          window.location.href = '/'
        }
        return Promise.reject(error)
      }
    )
  }

  async login(credentials) {
    return this.api.post('/login', credentials)
  }

  async register(userInfo) {
    return this.api.post('/register', userInfo)
  }

  async getProfile() {
    return this.api.get('/profile')
  }
}

export const authService = new AuthService()