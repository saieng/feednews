<template>
  <div class="relative overflow-hidden">
    <!-- 导航栏 -->
    <nav class="fixed top-0 left-0 right-0 z-50 bg-black bg-opacity-50 backdrop-blur-sm">
      <div class="container mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <!-- 导航按钮 -->
          <div class="flex space-x-8 items-center">
            <div class="relative flex flex-col items-center">
              <button @click="scrollToSection('intro')"
                :class="[currentSection === 'intro' ? 'text-white' : 'text-gray-400']"
                class="px-4 py-2 text-sm font-medium transition-colors hover:text-white focus:outline-none flex items-center">
                Introduction
              </button>
              <!-- 进度条 -->
              <div class="w-full h-1 bg-gray-700 rounded-full overflow-hidden mt-1">
                <div class="h-full bg-white transition-all duration-300" :style="{ width: `${scrollProgress}%` }"></div>
              </div>
            </div>
            <div class="relative">
              <button @click="scrollToSection('news')"
                :class="[currentSection === 'news' ? 'text-white' : 'text-gray-400']"
                class="px-4 py-2 text-sm font-medium transition-colors hover:text-white focus:outline-none flex items-center">
                News
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- 滚动容器 -->
    <div ref="scrollContainer" class="fixed inset-0 overflow-y-auto scroll-smooth" @wheel.prevent="handleWheel">
      <!-- 第一屏 - Introduction -->
      <section id="intro" class="relative min-h-screen flex items-center justify-center overflow-hidden">
        <!-- 视频背景 -->
        <video autoplay muted loop class="absolute inset-0 w-full h-full object-cover">
          <source src="/src/static/video/intro.mp4" type="video/mp4">
        </video>

        <!-- 视频遮罩 -->
        <div class="absolute inset-0 bg-black bg-opacity-40"></div>

        <!-- 粒子系统 -->
        <canvas ref="particleCanvas" class="absolute inset-0 w-full h-full z-10"></canvas>

        <!-- 滚动文本容器 -->
        <div
          class="relative z-20 w-full h-full flex flex-col justify-center items-center text-white px-8 overflow-hidden">
          <div ref="textContainer" class="text-center leading-relaxed w-full max-w-4xl"
            :style="{ transform: `translateY(${-textScrollOffset + windowHeight / 2}px)` }">
            <div v-for="(line, index) in textLines" :key="index" class="transition-all duration-300 ease-out" :style="{
              fontSize: getTextSize(index),
              opacity: getTextOpacity(index),
              marginBottom: '60px',
              fontWeight: getTextSize(index) === '2.5rem' ? '600' : '400'
            }">
              {{ line }}
            </div>
          </div>

          <!-- 滚动指示器 -->
          <div v-if="!textScrollComplete" class="absolute bottom-8 left-1/2 transform -translate-x-1/2 opacity-70">
            <div class="w-6 h-10 border-2 border-white rounded-full flex justify-center">
              <div class="w-1 h-3 bg-white rounded-full mt-2 animate-bounce"></div>
            </div>
            <p class="text-sm mt-2">Scroll to continue</p>
          </div>
        </div>
      </section>

      <!-- 第二屏 - News -->
      <section id="news" class="min-h-screen bg-gray-50 pt-20">
        <div class="container mx-auto px-4 py-8">
          <!-- 搜索栏 -->
          <div class="mb-8">
            <div class="max-w-2xl mx-auto">
              <div class="relative">
                <input v-model="searchQuery" type="text" placeholder="搜索新闻..."
                  class="w-full px-6 py-4 pr-12 text-lg rounded-full border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white bg-opacity-90 backdrop-blur-sm transition-all duration-300 hover:shadow-lg"
                  @input="handleSearch">
                <svg class="absolute left-4 top-1/2 transform -translate-y-1/2 w-6 h-6 text-gray-400" fill="none"
                  stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                </svg>
                <button v-if="searchQuery" @click="clearSearch"
                  class="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12">
                    </path>
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- 新闻网格 -->
          <NewsGrid :news-list="newsList" :is-loading="isLoading" :error="error" :has-more="hasMore"
            @load-more="loadMoreNews" @retry="fetchNews" />
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useNewsStore } from '@/store/news'
import NewsGrid from '@/components/news/NewsGrid.vue'

const newsStore = useNewsStore()

const searchQuery = ref('')
const isLoading = ref(false)
const error = ref(null)
const scrollY = ref(0)
const scrollContainer = ref(null)
const particleCanvas = ref(null)
const animationFrame = ref(null)
const currentSection = ref('intro')
const scrollProgress = ref(0)
const textScrollOffset = ref(0)
const textScrollComplete = ref(false)
const textContainer = ref(null)
const windowHeight = ref(800)

// 滚动文本内容
const textLines = [
  'When you want something,',
  '',
  '',
  'all the universe conspires',
  'in helping you to achieve it.',
  '',
  'Paulo Coelho',
  '',
  '',
  '',
  'Feed is that conspiracy:',
  'the conspiracy of trust.',
  '',
  '',
  '',
  'Trust is the single',
  'most important ingredient',
  'missing from digital relationships.',
  '',
  '',
  '',
  'Boston Consulting Group',
  'and the World Economic Forum',
  'forecast the digital economy to',
  'be worth between',
  '1.5 and 2.5 trillion dollars',
  'by 2016.',
  '',
  '',
  '',
  'The difference',
  'between those numbers',
  'is trust.',
  '',
  '',
  '',
  'Feed is a digital mechanism of trust'
]

// 文本滚动效果计算
const getTextSize = (index) => {
  const centerLineIndex = textScrollOffset.value / 60;
  const signedDistance = index - centerLineIndex;

  let size;
  if (signedDistance >= 0) { // 中心及下方
    // 从下方到中心，字体逐渐变大
    size = 1 + (2.5 - 1) * (1 - signedDistance / 4);
  } else { // 中心上方
    // 从中心到上方，字体继续变大
    size = 2.5 + Math.abs(signedDistance) * 0.8;
  }

  return `${Math.max(1, Math.min(4.5, size))}rem`;
};

const getTextOpacity = (index) => {
  const centerLineIndex = textScrollOffset.value / 60;
  const signedDistance = index - centerLineIndex;

  let opacity;
  if (signedDistance >= 0) { // 中心及下方，逐渐变亮
    // 在接近中心时最亮
    opacity = 1 - (signedDistance / 5);
  } else { // 中心上方，逐渐变暗
    opacity = 1 - (Math.abs(signedDistance) / 3);
  }

  return Math.max(0, Math.min(1, opacity));
};

// 计算当前部分和滚动进度
const updateScrollInfo = () => {
  const container = scrollContainer.value;
  if (!container) return;

  const maxTextScroll = (textLines.length - 1) * 60;

  if (currentSection.value === 'intro') {
    scrollProgress.value = Math.round((textScrollOffset.value / maxTextScroll) * 100);

    if (textScrollOffset.value >= maxTextScroll) {
      if (!textScrollComplete.value) {
        textScrollComplete.value = true;
        scrollProgress.value = 100;
        // 延迟一小段时间再滚动到新闻区，让用户看到进度条满
        setTimeout(() => {
          scrollToSection('news');
        }, 300);
      }
    } else {
      textScrollComplete.value = false;
    }
  } else {
    const newsSection = container.querySelector('#news');
    const newsScrollTop = newsSection.offsetTop;
    const scrollHeight = container.scrollHeight - container.clientHeight;
    const newsScroll = Math.max(0, scrollY.value - newsScrollTop);
    const newsHeight = scrollHeight - newsScrollTop;
    scrollProgress.value = newsHeight > 0 ? Math.round((newsScroll / newsHeight) * 100) : 0;
  }

  // 根据滚动位置判断当前部分
  const newsSection = container.querySelector('#news');
  if (newsSection) {
    currentSection.value = scrollY.value >= newsSection.offsetTop - 100 ? 'news' : 'intro';
  }
};

// 滚动到指定部分
const scrollToSection = (section) => {
  const container = scrollContainer.value
  if (!container) return

  const targetSection = container.querySelector(
    section === 'intro' ? 'section:first-child' : 'section:nth-child(2)'
  )

  if (targetSection) {
    container.scrollTo({
      top: section === 'intro' ? 0 : targetSection.offsetTop,
      behavior: 'smooth'
    })
  }
}

// 粒子系统
class Particle {
  constructor(x, y, canvas) {
    this.x = x
    this.y = y
    this.canvas = canvas
    this.size = Math.random() * 3 + 1
    this.speedX = Math.random() * 3 - 1.5
    this.speedY = Math.random() * 3 - 1.5
    this.opacity = Math.random() * 0.5 + 0.3
    this.color = `hsl(${Math.random() * 60 + 240}, 70%, 70%)`
  }

  update() {
    this.x += this.speedX
    this.y += this.speedY
    if (this.size > 0.2) this.size -= 0.1
    if (this.opacity > 0) this.opacity -= 0.01
  }

  draw(ctx) {
    ctx.save()
    ctx.globalAlpha = this.opacity
    ctx.fillStyle = this.color
    ctx.beginPath()
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2)
    ctx.fill()
    ctx.restore()
  }
}

let particles = []
let ctx = null

const newsList = computed(() => newsStore.newsList || [])
const hasMore = computed(() => newsStore.hasMore)

let isWheeling = false;
let wheelTimeout = null;

const handleWheel = (event) => {
  if (currentSection.value !== 'intro' || isWheeling) return;

  isWheeling = true;
  clearTimeout(wheelTimeout);
  wheelTimeout = setTimeout(() => {
    isWheeling = false;
  }, 500); // 增加防抖时间，减慢滚动响应

  const maxTextScroll = (textLines.length - 1) * 60;
  const scrollStep = 60; // 每次滚动的步长

  if (event.deltaY > 0) {
    // 向下滚动
    textScrollOffset.value = Math.min(textScrollOffset.value + scrollStep, maxTextScroll);
  } else {
    // 向上滚动
    textScrollOffset.value = Math.max(textScrollOffset.value - scrollStep, 0);
  }
  updateScrollInfo();
};

const handleScroll = (event) => {
  scrollY.value = event.target.scrollTop;
  // 只有在新闻区才需要更新滚动信息
  if (currentSection.value === 'news') {
    updateScrollInfo();
  }
};

const initParticleSystem = () => {
  const canvas = particleCanvas.value
  if (!canvas) return

  ctx = canvas.getContext('2d')
  canvas.width = window.innerWidth
  canvas.height = window.innerHeight

  // 创建初始粒子
  for (let i = 0; i < 50; i++) {
    particles.push(new Particle(
      Math.random() * canvas.width,
      Math.random() * canvas.height,
      canvas
    ))
  }

  const animate = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    // 更新和绘制粒子
    particles.forEach((particle, index) => {
      particle.update()
      particle.draw(ctx)

      // 移除消失的粒子
      if (particle.opacity <= 0 || particle.size <= 0.2) {
        particles.splice(index, 1)
      }
    })

    // 添加新粒子
    if (particles.length < 50 && Math.random() < 0.1) {
      particles.push(new Particle(
        Math.random() * canvas.width,
        Math.random() * canvas.height,
        canvas
      ))
    }

    animationFrame.value = requestAnimationFrame(animate)
  }

  animate()
}

const fetchNews = async (page = 1) => {
  isLoading.value = true
  error.value = null

  const result = await newsStore.fetchNews(page, 12)
  if (!result.success) {
    error.value = result.error
  }
  isLoading.value = false
}

const loadMoreNews = async () => {
  if (isLoading.value || !hasMore.value) return

  isLoading.value = true
  const result = await newsStore.loadMoreNews()
  if (!result.success) {
    error.value = result.error
  }
  isLoading.value = false
}

const handleSearch = () => {
  // 简单的防抖搜索
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    fetchNews(1)
  }, 300)
}

const clearSearch = () => {
  searchQuery.value = ''
  fetchNews(1)
}

const handleResize = () => {
  windowHeight.value = window.innerHeight
  if (particleCanvas.value) {
    particleCanvas.value.width = window.innerWidth
    particleCanvas.value.height = window.innerHeight
  }
}

let searchTimeout = null

// 键盘快捷键处理
const handleKeyPress = (event) => {
  // Alt + 1 切换到 Introduction
  if (event.altKey && event.key === '1') {
    scrollToSection('intro')
  }
  // Alt + 2 切换到 News
  if (event.altKey && event.key === '2') {
    scrollToSection('news')
  }
}

onMounted(() => {
  windowHeight.value = window.innerHeight;
  if (newsStore.newsList.length === 0) {
    fetchNews();
  }
  nextTick(() => {
    initParticleSystem();
    updateScrollInfo(); // 初始化滚动信息
  });
  window.addEventListener('resize', handleResize);
  window.addEventListener('keydown', handleKeyPress); // 添加键盘事件监听
  scrollContainer.value.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
  if (animationFrame.value) {
    cancelAnimationFrame(animationFrame.value);
  }
  window.removeEventListener('resize', handleResize);
  window.removeEventListener('keydown', handleKeyPress); // 移除键盘事件监听
  if (scrollContainer.value) {
    scrollContainer.value.removeEventListener('scroll', handleScroll);
  }
});

// 监听搜索词变化
watch(searchQuery, () => {
  handleSearch()
})
</script>