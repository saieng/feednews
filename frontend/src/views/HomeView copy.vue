<template>
  <div class="relative overflow-hidden">
    <!-- Logo动画 -->
    <div v-if="showLogo"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-80 transition-opacity duration-500"
      :class="{ 'opacity-0': logoFadeOut }">
      <div class="relative">
        <svg class="w-32 h-32 md:w-48 md:h-48 transition-transform duration-1000 ease-in-out" :class="{
          'scale-125': logoScale,
          'scale-75': !logoScale
        }" viewBox="0 0 165.774 197.826">
          <g>
            <path fill="#ffffff" d="M158.903,94.998L24.541,2.75c-7.14-4.9-16.889-3.07-21.789,4.046c-4.899,7.137-3.078,16.895,4.05,21.798
              l112.648,77.838l-90.363,49.234v-47.938h24.581L1.335,39.564v50.134v19.201v73.252c0,5.54,1.857,10.669,6.637,13.49
              c2.461,1.459,4.688,2.185,7.441,2.185c2.593,0,4.935-0.643,7.288-1.941l135.008-74.232c4.774-2.621,7.768-7.521,8.047-12.959
              C166.019,103.271,163.386,98.082,158.903,94.998" />
          </g>
        </svg>
      </div>
    </div>


    <!-- 导航栏 -->
    <nav v-show="!showLogo" class="fixed top-0 left-0 right-0 z-50 bg-black bg-opacity-50 backdrop-blur-sm">
      <div class="container mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <!-- 导航按钮 -->
          <div class="flex space-x-8 items-center">
            <div class="relative flex flex-col items-center">
              <button @click="scrollToSection('intro', 'click')"
                :class="[currentSection === 'intro' ? 'text-white' : 'text-gray-400']"
                class="px-4 py-2 text-sm font-medium transition-colors hover:text-white focus:outline-none flex items-center">
                Introduction
              </button>
              <!-- 进度条 - 只在第一屏显示 -->
              <div v-if="currentSection === 'intro'" class="w-full h-1 bg-gray-700 rounded-full overflow-hidden mt-1">
                <div class="h-full bg-white transition-all duration-300" :style="{ width: `${scrollProgress}%` }"></div>
              </div>
            </div>
            <div class="relative flex flex-col items-center">
              <button @click="scrollToSection('news', 'click')"
                :class="[currentSection === 'news' ? 'text-white' : 'text-gray-400']"
                class="px-4 py-2 text-sm font-medium transition-colors hover:text-white focus:outline-none flex items-center">
                News
              </button>
              <!-- 进度条 - 只在第二屏显示 -->
              <div v-if="currentSection === 'news'" class="w-full h-1 bg-gray-700 rounded-full overflow-hidden mt-1">
                <div class="h-full bg-white transition-all duration-300" :style="{ width: `${scrollProgress}%` }"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- 滚动容器 -->
    <div ref="scrollContainer" class="fixed inset-0 overflow-y-auto scroll-smooth" @wheel.prevent="handleWheel"
      @touchstart="handleTouchStart" @touchmove="handleTouchMove" @touchend="handleTouchEnd">
      <!-- 第一屏 - Introduction -->
      <section id="intro" class="relative min-h-screen flex items-center justify-center overflow-hidden"
        :class="{ 'opacity-0': showLogo }">
        <!-- 视频背景 -->
        <video autoplay muted loop class="absolute inset-0 w-full h-full object-cover">
          <source src="/src/static/video/intro.mp4" type="video/mp4">
        </video>

        <!-- 视频遮罩 -->
        <div class="absolute inset-0 bg-black bg-opacity-40"></div>

        <!-- 粒子系统 -->
        <canvas ref="particleCanvas" class="absolute inset-0 w-full h-full z-10"></canvas>

        <!-- 滚动文本容器 -->
        <div ref="textContainer"
          class="absolute inset-0 flex flex-col justify-center items-center text-white z-20 overflow-hidden">
          <div v-for="(line, index) in textLines" :key="index"
            class="absolute left-0 right-0 text-center font-light transition-all duration-300 ease-out" :style="{
              fontSize: getTextSize(index),
              opacity: getTextOpacity(index),
              transform: `translateY(${getTextTransform(index)}px)`,
              textShadow: '0 0 10px rgba(0, 0, 255, 0.5)',
              whiteSpace: 'nowrap'
            }">
            {{ line }}
          </div>
        </div>

        <!-- 滚动指示器 - 固定在底部，可点击 -->
        <div
          class="fixed bottom-8 left-1/2 transform -translate-x-1/2 z-30 cursor-pointer transition-all duration-300 hover:scale-110"
          @click="handleScrollIndicatorClick">
          <div
            class="w-6 h-10 border-2 border-white rounded-full flex justify-center bg-black bg-opacity-20 backdrop-blur-sm">
            <div class="w-1 h-3 bg-white rounded-full mt-2"
              :class="textScrollComplete ? 'opacity-50' : 'animate-bounce'"></div>
          </div>
          <p class="text-sm mt-2 text-center">{{ textScrollComplete ? 'Enter News' : 'Scroll to continue' }}</p>
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
const currentSection = ref('intro')
const scrollProgress = ref(0)
const textScrollOffset = ref(0)
const textScrollComplete = ref(false)

// Logo动画相关状态
const showLogo = ref(true)
const logoFadeOut = ref(false)
const logoScale = ref(true)
let logoInterval = null
const animationFrame = ref(null)
const textContainer = ref(null)
const windowHeight = ref(800)

// 触摸事件相关
const touchStartY = ref(0)
const touchStartTime = ref(0)
const isTouching = ref(false)

// 切换方式记录
const switchMethod = ref('') // 'scroll' | 'click' | 'auto'
const previousTextScrollOffset = ref(0) // 记录之前的具体文字行偏移

// 滚动文本内容 - 去除空行，连续显示
const textLines = [
  'When you want something,',
  'all the universe conspires',
  'in helping you to achieve it.',
  'Paulo Coelho',
  'Feed is that conspiracy:',
  'the conspiracy of trust.',
  'Trust is the single',
  'most important ingredient',
  'missing from digital relationships.',
  'Boston Consulting Group',
  'and the World Economic Forum',
  'forecast the digital economy to',
  'be worth between',
  '1.5 and 2.5 trillion dollars',
  'by 2016.',
  'The difference',
  'between those numbers',
  'is trust.',
  'Feed is a digital mechanism of trust'
]

// 文本滚动效果计算 - 平滑连续的文字变化效果
const getTextSize = (index) => {
  const progress = textScrollOffset.value;
  const offset = index - progress;

  // 当前行或接近当前行
  if (Math.abs(offset) < 0.3) {
    return '3.2rem';
  }
  // 屏幕中间以上的文字（offset < 0）向上滚动时继续放大
  else if (offset < 0 && offset > -1.5) {
    // 向上滚动的文字，距离越远放大越多
    const factor = Math.abs(offset) / 1.5;
    const size = 3.2 + factor * 1.5; // 从3.2rem放大到4.7rem
    return `${size}rem`;
  }
  // 屏幕中间以下的文字正常处理
  else if (offset > 0 && offset < 0.8) {
    const factor = 1 - (offset / 0.8);
    const size = 1.0 + factor * 2.2;
    return `${size}rem`;
  }
  else if (Math.abs(offset) < 1.2) {
    return '1.3rem';
  } else {
    return '1.0rem';
  }
};

const getTextOpacity = (index) => {
  const progress = textScrollOffset.value;
  const distance = Math.abs(index - progress);

  // 基于距离计算透明度，距离越近透明度越高，更快速的变化
  if (distance < 0.3) {
    return 1;
  } else if (distance < 0.8) {
    // 线性插值计算中间状态，更快速的透明度变化
    const factor = 1 - (distance / 0.8);
    return 0.2 + factor * 0.8;
  } else if (distance < 1.2) {
    return 0.3;
  } else if (distance < 2.0) {
    return 0.15;
  } else {
    return 0;
  }
};

// 文本垂直变换效果 - 确保当前文字在屏幕中心，屏幕中间以上的文字向上滚动到顶部消失
const getTextTransform = (index) => {
  const progress = textScrollOffset.value;
  const offset = (index - progress) * 50; // 行间距50px

  // 如果文字在屏幕中间以上（offset < 0），让它们继续向上移动并放大
  if (offset < 0) {
    // 向上滚动的文字，距离越远向上移动越多
    return offset * 1.5; // 加速向上移动
  }

  return offset;
};

// 计算当前部分和滚动进度
const updateScrollInfo = () => {
  const container = scrollContainer.value;
  if (!container) return;

  // 更新最大滚动值以适应新的逐行滚动算法
  const maxTextScroll = textLines.length - 1;
  const newsSection = container.querySelector('#news');

  // 根据滚动位置判断当前部分
  if (newsSection) {
    const isInNewsSection = scrollY.value >= newsSection.offsetTop - 100;
    currentSection.value = isInNewsSection ? 'news' : 'intro';

    if (currentSection.value === 'intro') {
      // 在第一屏时，根据文本滚动偏移计算进度
      scrollProgress.value = Math.round((textScrollOffset.value / maxTextScroll) * 100);

      if (textScrollOffset.value >= maxTextScroll) {
        if (!textScrollComplete.value) {
          textScrollComplete.value = true;
          scrollProgress.value = 100;
          // 快速自动切换到第二屏
          setTimeout(() => {
            scrollToSection('news');
          }, 500);
        }
      } else {
        textScrollComplete.value = false;
      }
    } else {
      // 在第二屏时，根据实际滚动位置计算进度
      const newsScrollTop = newsSection.offsetTop;
      const scrollHeight = container.scrollHeight - container.clientHeight;
      const newsScroll = Math.max(0, scrollY.value - newsScrollTop);
      const newsHeight = scrollHeight - newsScrollTop;
      scrollProgress.value = newsHeight > 0 ? Math.round((newsScroll / newsHeight) * 100) : 0;
    }
  }
};

// 滚动到指定部分
const scrollToSection = (section, method = 'auto') => {
  const container = scrollContainer.value
  if (!container) return

  switchMethod.value = method;

  if (section === 'intro') {
    // 滚动到第一屏，根据切换方式设置不同状态
    const maxTextScroll = textLines.length - 1;
    if (method === 'scroll') {
      // 通过鼠标滚动切换回第一屏，设置为100%（最后一行文字）
      textScrollOffset.value = maxTextScroll;
      textScrollComplete.value = true;
      scrollProgress.value = 100;
    } else if (method === 'click') {
      // 通过点击指示器切换，保留之前的具体文字行偏移
      textScrollOffset.value = previousTextScrollOffset.value;
      textScrollComplete.value = previousTextScrollOffset.value >= maxTextScroll;
      scrollProgress.value = Math.round((previousTextScrollOffset.value / maxTextScroll) * 100);
    }
    container.scrollTo({
      top: 0,
      behavior: 'smooth'
    })
  } else {
    // 切换到第二屏前，记录当前的具体文字行偏移
    previousTextScrollOffset.value = textScrollOffset.value;
    const targetSection = container.querySelector('#news')
    if (targetSection) {
      container.scrollTo({
        top: targetSection.offsetTop,
        behavior: 'smooth'
      })
    }
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
  if (isWheeling) return;

  // 在第一屏处理文本滚动
  if (currentSection.value === 'intro') {
    isWheeling = true;
    clearTimeout(wheelTimeout);
    wheelTimeout = setTimeout(() => {
      isWheeling = false;
    }, 10); // 减少防抖时间，提高灵敏度

    const maxTextScroll = textLines.length - 1;
    const scrollStep = 0.24; // 滚动速度再提升3倍

    if (event.deltaY > 0) {
      // 向下滚动
      if (textScrollOffset.value >= maxTextScroll && textScrollComplete.value) {
        // 如果已经滚动到100%，继续向下滚动则切换到第二屏
        scrollToSection('news');
      } else {
        textScrollOffset.value = Math.min(textScrollOffset.value + scrollStep, maxTextScroll);
      }
    } else {
      // 向上滚动
      textScrollOffset.value = Math.max(textScrollOffset.value - scrollStep, 0);
    }
    updateScrollInfo();
  }
  // 在第二屏处理页面回滚
  else if (currentSection.value === 'news' && event.deltaY < 0) {
    // 向上滚动时，如果已经在第二屏顶部，则切换回第一屏
    const container = scrollContainer.value;
    const newsSection = container?.querySelector('#news');
    if (newsSection && scrollY.value <= newsSection.offsetTop + 50) {
      scrollToSection('intro', 'click');
    }
  }
};

// 触摸事件处理
const handleTouchStart = (event) => {
  if (currentSection.value !== 'intro') return;

  touchStartY.value = event.touches[0].clientY;
  touchStartTime.value = Date.now();
  isTouching.value = true;
};

const handleTouchMove = (event) => {
  if (currentSection.value !== 'intro' || !isTouching.value) return;

  event.preventDefault(); // 防止页面滚动
};

const handleTouchEnd = (event) => {
  if (currentSection.value !== 'intro' || !isTouching.value) return;

  const touchEndY = event.changedTouches[0].clientY;
  const touchEndTime = Date.now();
  const deltaY = touchStartY.value - touchEndY;
  const deltaTime = touchEndTime - touchStartTime.value;

  // 只有在快速滑动时才触发文本滚动
  if (Math.abs(deltaY) > 30 && deltaTime < 300) {
    const maxTextScroll = textLines.length - 1;
    const scrollStep = 2.4; // 触摸滚动速度也提升3倍

    if (deltaY > 0) {
      // 向上滑动（向下滚动文本）
      textScrollOffset.value = Math.min(textScrollOffset.value + scrollStep, maxTextScroll);
    } else {
      // 向下滑动（向上滚动文本）
      textScrollOffset.value = Math.max(textScrollOffset.value - scrollStep, 0);
    }
    updateScrollInfo();
  }

  isTouching.value = false;
};

// 滚动指示器点击事件
const handleScrollIndicatorClick = () => {
  // 保存当前进度，然后直接跳转到第二屏
  previousTextScrollOffset.value = textScrollOffset.value;
  scrollToSection('news', 'click');
};


const handleScroll = (event) => {
  scrollY.value = event.target.scrollTop;

  // 始终更新滚动信息，以便正确处理区域切换
  updateScrollInfo();
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

  // 启动logo动画
  logoInterval = setInterval(() => {
    logoScale.value = !logoScale.value;
  }, 1000); // 每秒切换一次缩放状态

  // 5秒后开始淡出logo
  setTimeout(() => {
    logoFadeOut.value = true;
    // 淡出动画完成后隐藏logo
    setTimeout(() => {
      showLogo.value = false;
    }, 500);
  }, 5000);

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
  // 清理logo动画定时器
  if (logoInterval) {
    clearInterval(logoInterval);
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
