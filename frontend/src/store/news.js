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
    async fetchNews(page = 1, limit = 12) {
      this.isLoading = true
      try {
        // 模拟API延迟
        await new Promise(resolve => setTimeout(resolve, 800))
        
        // 模拟新闻数据
        const mockNews = this.generateMockNews(page, limit)
        
        if (page === 1) {
          this.newsList = mockNews.news
        } else {
          this.newsList.push(...mockNews.news)
        }
        
        this.currentPage = page
        this.totalNews = mockNews.total
        this.hasMore = this.newsList.length < this.totalNews
        
        return { success: true }
      } catch (error) {
        return { 
          success: false, 
          error: error.response?.data?.message || '获取新闻失败' 
        }
      } finally {
        this.isLoading = false
      }
    },

    async loadMoreNews() {
      if (!this.hasMore || this.isLoading) return
      
      const nextPage = this.currentPage + 1
      return await this.fetchNews(nextPage)
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

    // 生成模拟新闻数据
    generateMockNews(page = 1, limit = 12) {
      const mockTitles = [
        '人工智能技术在医疗领域的最新突破',
        '全球气候变化对经济发展的深远影响',
        '新能源汽车市场迎来爆发式增长',
        '5G技术推动智慧城市建设进入新阶段',
        '量子计算机研发取得重大进展',
        '区块链技术在金融行业的创新应用',
        '太空探索计划开启人类新纪元',
        '生物技术革命改变传统农业模式',
        '虚拟现实技术重塑教育行业格局',
        '可持续发展成为企业战略重点',
        '数字货币监管政策日趋完善',
        '机器学习算法优化供应链管理',
        '清洁能源投资创历史新高',
        '基因编辑技术带来医学新希望',
        '物联网设备安全问题引发关注',
        '自动驾驶技术商业化进程加速',
        '云计算服务市场竞争日益激烈',
        '人工智能伦理问题亟待解决',
        '新材料技术推动制造业升级',
        '数字化转型成为企业必修课'
      ]

      const mockDescriptions = [
        '最新研究表明，人工智能在疾病诊断和治疗方案制定方面展现出巨大潜力，有望彻底改变传统医疗模式。',
        '专家分析指出，气候变化不仅影响环境，更对全球经济结构产生深刻影响，各国需要制定相应对策。',
        '随着技术不断成熟和政策支持力度加大，新能源汽车正迎来前所未有的发展机遇。',
        '5G网络的大规模部署为智慧城市建设提供了强有力的技术支撑，城市管理效率显著提升。',
        '科学家在量子计算领域取得重要突破，为解决复杂计算问题开辟了新的可能性。',
        '金融机构积极探索区块链技术应用，在提高交易效率和安全性方面取得显著成效。',
        '多国联合推进的太空探索项目正在改写人类对宇宙的认知，开启探索新时代。',
        '基因工程和生物技术的发展为农业生产带来革命性变化，作物产量和品质大幅提升。',
        'VR技术在教育领域的应用越来越广泛，为学生提供了更加生动直观的学习体验。',
        '越来越多的企业将可持续发展纳入核心战略，积极承担社会责任。'
      ]

      const mockAuthors = [
        '张明', '李华', '王强', '刘芳', '陈杰',
        '赵敏', '孙涛', '周莉', '吴刚', '郑雪'
      ]

      const startIndex = (page - 1) * limit
      const news = []
      
      for (let i = 0; i < limit; i++) {
        const index = startIndex + i
        if (index >= 50) break // 模拟总共50条新闻
        
        news.push({
          id: index + 1,
          title: mockTitles[index % mockTitles.length],
          description: mockDescriptions[index % mockDescriptions.length],
          image_url: `https://picsum.photos/400/225?random=${index + 1}`,
          creator: {
            username: mockAuthors[index % mockAuthors.length]
          },
          author: mockAuthors[index % mockAuthors.length],
          created_at: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString(),
          category: ['科技', '经济', '社会', '环境', '健康'][index % 5]
        })
      }
      
      return {
        news,
        total: 50,
        page,
        limit
      }
    },
  },
})