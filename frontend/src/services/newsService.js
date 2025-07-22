import axios from 'axios'

const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

class NewsService {
  constructor() {
    this.api = axios.create({
      baseURL: `${API_URL}/news`,
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
      (error) => Promise.reject(error)
    )
  }

  async getNews({ page = 1, limit = 12, q = null } = {}) {
    const params = { page, limit }
    if (q) params.q = q
    
    return this.api.get('/', { params })
  }

  async getNewsById(id) {
    return this.api.get(`/${id}`)
  }

  async createNews(newsData) {
    return this.api.post('/', newsData)
  }

  async updateNews(id, newsData) {
    return this.api.put(`/${id}`, newsData)
  }

  async deleteNews(id) {
    return this.api.delete(`/${id}`)
  }

  async uploadImage(file) {
    const formData = new FormData()
    formData.append('image', file)
    
    return this.api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  }
}

export const newsService = new NewsService()