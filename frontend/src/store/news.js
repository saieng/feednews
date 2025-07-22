import { defineStore } from 'pinia'
import { newsService } from '@/services/newsService'

export const useNewsStore = defineStore('news', {
  state: () => ({
    newsList: [],
    currentPage: 1,
    totalNews: 0,
    isLoading: false,
    hasMore: true,
  }),

  actions: {
    async fetchNews(page = 1, limit = 12, searchQuery = null) {
      this.isLoading = true
      try {
        const response = await newsService.getNews({ page, limit, q: searchQuery })
        const data = response.data
        
        if (page === 1) {
          this.newsList = data.items
        } else {
          this.newsList.push(...data.items)
        }
        
        this.currentPage = page
        this.totalNews = data.total
        this.hasMore = this.newsList.length < this.totalNews
        
        return { success: true }
      } catch (error) {
        return { 
          success: false, 
          error: error.response?.data?.detail || error.message || '获取新闻失败' 
        }
      } finally {
        this.isLoading = false
      }
    },

    async loadMoreNews(searchQuery = null) {
      if (!this.hasMore || this.isLoading) return
      
      const nextPage = this.currentPage + 1
      return await this.fetchNews(nextPage, 12, searchQuery)
    },

    async searchNews(query) {
      return await this.fetchNews(1, 12, query)
    },

    async createNews(newsData) {
      try {
        const response = await newsService.createNews(newsData)
        this.newsList.unshift(response.data)
        this.totalNews += 1
        return { success: true, data: response.data }
      } catch (error) {
        return { 
          success: false, 
          error: error.response?.data?.message || '创建新闻失败' 
        }
      }
    },

    async updateNews(id, newsData) {
      try {
        const response = await newsService.updateNews(id, newsData)
        const index = this.newsList.findIndex(news => news.id === id)
        if (index !== -1) {
          this.newsList[index] = response.data
        }
        return { success: true, data: response.data }
      } catch (error) {
        return { 
          success: false, 
          error: error.response?.data?.message || '更新新闻失败' 
        }
      }
    },

    async deleteNews(id) {
      try {
        await newsService.deleteNews(id)
        this.newsList = this.newsList.filter(news => news.id !== id)
        this.totalNews -= 1
        return { success: true }
      } catch (error) {
        return { 
          success: false, 
          error: error.response?.data?.message || '删除新闻失败' 
        }
      }
    },

    async getNewsById(id) {
      try {
        const response = await newsService.getNewsById(id)
        return response.data
      } catch (error) {
        console.error('获取新闻详情失败:', error)
        throw error
      }
    },


  },
})