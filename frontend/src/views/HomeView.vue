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
          
          <!-- 用户认证区域 -->
          <div class="flex items-center space-x-4">
            <!-- 未登录状态 -->
            <div v-if="!authStore.isLoggedIn" class="flex items-center space-x-2">
              <button 
                @click="openAuthModal"
                class="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-black"
              >
                登录 / 注册
              </button>
            </div>
            
            <!-- 已登录状态 -->
            <div v-else class="flex items-center space-x-3">
              <button 
                @click="goToAdmin"
                class="text-white text-sm hover:text-blue-300 transition-colors cursor-pointer underline decoration-dotted underline-offset-4"
              >
                欢迎，{{ authStore.user?.username || authStore.user?.email }}
              </button>
              <button 
                @click="handleLogout"
                class="px-4 py-2 text-sm font-medium text-gray-300 hover:text-white border border-gray-600 hover:border-gray-400 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 focus:ring-offset-black"
              >
                退出登录
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- 白色过渡层 -->
      <div v-if="isTransitioning && whiteScreenVisible" 
        class="fixed inset-0 z-40 bg-white transition-all duration-500 ease-in-out"
        :style="{
          transform: whiteScreenTransform,
          opacity: 1
        }"
      ></div>
      
      <!-- 紫色过渡层 -->
      <div v-if="isTransitioning && purpleScreenVisible" 
        class="fixed inset-0 z-50 bg-purple-600 transition-all duration-500 ease-in-out"
        :style="{
          transform: purpleScreenTransform,
          opacity: 1
        }"
      ></div>

    <!-- 滚动容器 -->
    <div v-show="!showLogo" ref="scrollContainer" class="fixed inset-0" 
      style="overflow: hidden; scrollbar-width: none; -ms-overflow-style: none;"
      @wheel="handleWheel" @scroll="handleScroll" @touchstart="handleTouchStart" @touchmove="handleTouchMove" @touchend="handleTouchEnd">
      <!-- 第一屏 - Introduction -->
      <section id="intro" class="absolute inset-0 flex items-center justify-center overflow-hidden transition-all duration-1000 ease-out text-smooth no-select"
        :class="{ 
          'opacity-0': showLogo,
          'opacity-100 translate-y-0 scale-100': currentSection === 'intro' && !isTransitioning,
          'opacity-0 -translate-y-full scale-95': currentSection === 'news' && !isTransitioning,
          'opacity-0': isTransitioning
        }">
        <!-- 视频背景 -->
        <video autoplay muted loop class="absolute inset-0 w-full h-full object-cover">
          <source src="/static/video/intro.mp4" type="video/mp4">
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

        <!-- 滚动指示器 - 固定在底部，可点击，只在第一屏显示 -->
        <div
          v-show="currentSection === 'intro'"
          class="fixed bottom-8 left-1/2 transform -translate-x-1/2 z-30 cursor-pointer transition-all duration-300 hover:scale-110 flex flex-col items-center"
          @click="handleScrollIndicatorClick">
          <div
            class="w-6 h-10 border-2 border-white rounded-full flex justify-center bg-black bg-opacity-20 backdrop-blur-sm">
            <div class="w-1 h-3 bg-white rounded-full mt-2"
              :class="textScrollComplete ? 'opacity-50' : 'animate-bounce'"></div>
          </div>
          <p class="text-sm mt-2 text-center whitespace-nowrap text-white">{{ textScrollComplete ? 'Enter News' : 'Scroll to continue' }}</p>
        </div>
      </section>

      <!-- 第二屏 - News -->
      <section id="news" class="absolute inset-0 bg-gray-50 pt-20 transition-all duration-1000 ease-out overflow-y-auto text-smooth"
        style="scrollbar-width: thin; scrollbar-color: #cbd5e0 #f7fafc;"
        @scroll="handleNewsScroll"
        :class="{
          'opacity-100 translate-y-0 scale-100': currentSection === 'news' && !isTransitioning,
          'opacity-0 translate-y-full scale-95': currentSection === 'intro' && !isTransitioning,
          'opacity-0': isTransitioning
        }">
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
    
    <!-- 认证模态框 -->
    <AuthModal 
      :is-open="showAuthModal" 
      @close="closeAuthModal" 
      @success="handleAuthSuccess" 
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useNewsStore } from '@/store/news'
import { useAuthStore } from '@/store/auth'
import NewsGrid from '@/components/news/NewsGrid.vue'
import AuthModal from '@/components/auth/AuthModal.vue'

const router = useRouter()
const newsStore = useNewsStore()
const authStore = useAuthStore()

// 认证相关状态
const showAuthModal = ref(false)

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

// 粒子系统变量
let particles = []
let ctx = null

// 触摸事件相关
const touchStartY = ref(0)
const touchStartTime = ref(0)
const isTouching = ref(false)

// 切换方式记录
const switchMethod = ref('') // 'scroll' | 'click' | 'auto'
const previousTextScrollOffset = ref(0) // 记录之前的具体文字行偏移
const savedIntroProgress = ref(0) // 保存的introduction进度
const newsScrollY = ref(0) // News页面的滚动位置

// 过渡状态
const isTransitioning = ref(false)
const transitionDirection = ref('down') // 'down' 或 'up'

// 白色和紫色屏幕状态
const whiteScreenVisible = ref(false)
const purpleScreenVisible = ref(false)
const whiteScreenTransform = ref('translateY(-100%)')
const purpleScreenTransform = ref('translateY(-100%)')

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

// 文本滚动效果计算 - 平滑连续的文字变化效果，适配手机端
const getTextSize = (index) => {
  const progress = textScrollOffset.value;
  const offset = index - progress;
  const isMobile = window.innerWidth < 768;
  
  // 根据设备类型调整基础尺寸
  const baseScale = isMobile ? 0.6 : 1; // 手机端缩小到60%

  // 当前行或接近当前行
  if (Math.abs(offset) < 0.3) {
    return `${3.2 * baseScale}rem`;
  }
  // 屏幕中间以上的文字（offset < 0）向上滚动时继续放大
  else if (offset < 0 && offset > -1.5) {
    // 向上滚动的文字，距离越远放大越多
    const factor = Math.abs(offset) / 1.5;
    const size = (3.2 + factor * 1.5) * baseScale; // 从3.2rem放大到4.7rem
    return `${size}rem`;
  }
  // 屏幕中间以下的文字正常处理
  else if (offset > 0 && offset < 0.8) {
    const factor = 1 - (offset / 0.8);
    const size = (1.0 + factor * 2.2) * baseScale;
    return `${size}rem`;
  }
  else if (Math.abs(offset) < 1.2) {
    return `${1.3 * baseScale}rem`;
  } else {
    return `${1.0 * baseScale}rem`;
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
  const maxTextScroll = textLines.length - 1;

  if (currentSection.value === 'intro') {
    // 在第一屏时，根据文本滚动偏移计算进度
    scrollProgress.value = Math.round((textScrollOffset.value / maxTextScroll) * 100);

    if (textScrollOffset.value >= maxTextScroll) {
      if (!textScrollComplete.value) {
        textScrollComplete.value = true;
        scrollProgress.value = 100;
        // 延迟自动切换到第二屏
        setTimeout(() => {
          if (currentSection.value === 'intro' && !isTransitioning.value) {
            scrollToSection('news', 'auto');
          }
        }, 800);
      }
    } else {
      textScrollComplete.value = false;
    }
  } else if (currentSection.value === 'news') {
    // 在第二屏时，根据滚动位置计算进度
    const newsSection = document.getElementById('news');
    if (newsSection) {
      const scrollTop = newsSection.scrollTop;
      const scrollHeight = newsSection.scrollHeight - newsSection.clientHeight;
      if (scrollHeight > 0) {
        scrollProgress.value = Math.round((scrollTop / scrollHeight) * 100);
      } else {
        scrollProgress.value = 0;
      }
      newsScrollY.value = scrollTop;
    }
  }
};

// 滚动到指定部分 - 重新设计为纯色滑动效果
const scrollToSection = (section, method = 'auto') => {
  // 防止重复触发
  if (isTransitioning.value) return

  switchMethod.value = method;
  isTransitioning.value = true;
  
  // 设置过渡方向
  if (section === 'intro') {
    transitionDirection.value = 'up';
    previousTextScrollOffset.value = textScrollOffset.value;
  } else {
    transitionDirection.value = 'down';
    previousTextScrollOffset.value = textScrollOffset.value;
  }

  if (section === 'news') {
     // 保存当前introduction进度
     savedIntroProgress.value = textScrollOffset.value;
     
     // 向下切换到新闻页面
     // 第一步：白色屏幕滑入 (0-0.5秒)
     whiteScreenVisible.value = true;
     whiteScreenTransform.value = 'translateY(-100%)';
     
     setTimeout(() => {
       whiteScreenTransform.value = 'translateY(0%)';
     }, 100);
     
     // 第二步：紫色屏幕滑入覆盖白色 (0.5-1秒)
     setTimeout(() => {
       purpleScreenVisible.value = true;
       purpleScreenTransform.value = 'translateY(-100%)';
       
       setTimeout(() => {
         purpleScreenTransform.value = 'translateY(0%)';
       }, 100);
     }, 500);
     
     // 第三步：切换内容并退出 (1-2秒)
     setTimeout(() => {
       currentSection.value = section;
       // 重置News页面滚动位置
       newsScrollY.value = 0;
       nextTick(() => {
         const newsSection = document.getElementById('news');
         if (newsSection) {
           newsSection.scrollTop = 0;
         }
         updateScrollInfo();
       });
       
       whiteScreenTransform.value = 'translateY(100%)';
       purpleScreenTransform.value = 'translateY(100%)';
       
       setTimeout(() => {
         // 重置状态
         whiteScreenVisible.value = false;
         purpleScreenVisible.value = false;
         whiteScreenTransform.value = 'translateY(-100%)';
         purpleScreenTransform.value = 'translateY(-100%)';
         isTransitioning.value = false;
       }, 500);
     }, 1000);
  } else {
     // 向上切换到介绍页面
     // 第一步：白色屏幕滑入 (0-0.5秒)
     whiteScreenVisible.value = true;
     whiteScreenTransform.value = 'translateY(100%)';
     
     setTimeout(() => {
       whiteScreenTransform.value = 'translateY(0%)';
     }, 100);
     
     // 第二步：紫色屏幕滑入覆盖白色 (0.5-1秒)
     setTimeout(() => {
       purpleScreenVisible.value = true;
       purpleScreenTransform.value = 'translateY(100%)';
       
       setTimeout(() => {
         purpleScreenTransform.value = 'translateY(0%)';
       }, 100);
     }, 500);
     
     // 第三步：切换内容并退出 (1-2秒)
     setTimeout(() => {
       currentSection.value = section;
       const maxTextScroll = textLines.length - 1;
       
       // 恢复到保存的进度
       textScrollOffset.value = savedIntroProgress.value;
       textScrollComplete.value = savedIntroProgress.value >= maxTextScroll;
       scrollProgress.value = Math.round((savedIntroProgress.value / maxTextScroll) * 100);
       
       whiteScreenTransform.value = 'translateY(-100%)';
       purpleScreenTransform.value = 'translateY(-100%)';
       
       setTimeout(() => {
         // 重置状态
         whiteScreenVisible.value = false;
         purpleScreenVisible.value = false;
         whiteScreenTransform.value = 'translateY(100%)';
         purpleScreenTransform.value = 'translateY(100%)';
         isTransitioning.value = false;
       }, 500);
     }, 1000);
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

const newsList = computed(() => newsStore.newsList || [])
const hasMore = computed(() => newsStore.hasMore)

let isWheeling = false;
let wheelTimeout = null;

const handleWheel = (event) => {
  if (isWheeling || isTransitioning.value) return;
  
  // 在第一屏处理文本滚动
  if (currentSection.value === 'intro') {
    event.preventDefault(); // 只在intro页面阻止默认滚动
    
    isWheeling = true;
    clearTimeout(wheelTimeout);
    wheelTimeout = setTimeout(() => {
      isWheeling = false;
    }, 50); // 适中的防抖时间

    const maxTextScroll = textLines.length - 1;
    const scrollStep = 0.8; // 更平滑的滚动速度

    if (event.deltaY > 0) {
      // 向下滚动
      if (textScrollOffset.value >= maxTextScroll && textScrollComplete.value) {
        // 如果已经滚动到100%，继续向下滚动则切换到第二屏
        scrollToSection('news', 'scroll');
      } else {
        textScrollOffset.value = Math.min(textScrollOffset.value + scrollStep, maxTextScroll);
      }
    } else {
      // 向上滚动
      textScrollOffset.value = Math.max(textScrollOffset.value - scrollStep, 0);
    }
    updateScrollInfo();
  }
  // 在第二屏处理滚动和切换
  else if (currentSection.value === 'news') {
    const newsSection = document.getElementById('news');
    if (newsSection) {
      const scrollTop = newsSection.scrollTop;
      
      // 如果在顶部且向上滚动，切换回第一屏
      if (scrollTop === 0 && event.deltaY < 0) {
        event.preventDefault(); // 只在需要切换时阻止默认滚动
        isWheeling = true;
        clearTimeout(wheelTimeout);
        wheelTimeout = setTimeout(() => {
          isWheeling = false;
        }, 100);
        scrollToSection('intro', 'scroll');
      }
      // 其他情况允许正常滚动，不阻止默认行为
    }
  }
};

// 触摸事件处理
const handleTouchStart = (event) => {
  if (isTransitioning.value) return;

  touchStartY.value = event.touches[0].clientY;
  touchStartTime.value = Date.now();
  isTouching.value = true;
};

const handleTouchMove = (event) => {
  if (!isTouching.value || isTransitioning.value) return;

  event.preventDefault(); // 防止页面滚动
};

const handleTouchEnd = (event) => {
  if (!isTouching.value || isTransitioning.value) return;

  const touchEndY = event.changedTouches[0].clientY;
  const touchEndTime = Date.now();
  const deltaY = touchStartY.value - touchEndY;
  const deltaTime = touchEndTime - touchStartTime.value;

  // 快速滑动检测
  if (Math.abs(deltaY) > 50 && deltaTime < 300) {
    if (currentSection.value === 'intro') {
      const maxTextScroll = textLines.length - 1;
      const scrollStep = 3.0; // 触摸滚动步长

      if (deltaY > 0) {
        // 向上滑动（向下滚动文本）
        if (textScrollOffset.value >= maxTextScroll && textScrollComplete.value) {
          // 如果已经滚动到100%，继续向上滑动则切换到第二屏
          scrollToSection('news', 'touch');
        } else {
          textScrollOffset.value = Math.min(textScrollOffset.value + scrollStep, maxTextScroll);
        }
      } else {
        // 向下滑动（向上滚动文本）
        textScrollOffset.value = Math.max(textScrollOffset.value - scrollStep, 0);
      }
      updateScrollInfo();
    } else if (currentSection.value === 'news') {
      // 在第二屏时的滑动处理
      const newsSection = document.getElementById('news');
      if (newsSection && newsSection.scrollTop === 0 && deltaY < 0) {
        // 在顶部向下滑动时切换回第一屏
        scrollToSection('intro', 'touch');
      }
    }
  }

  isTouching.value = false;
};

// 滚动指示器点击事件
const handleScrollIndicatorClick = () => {
  if (isTransitioning.value) return;
  
  // 保存当前进度，然后直接跳转到第二屏
  savedIntroProgress.value = textScrollOffset.value;
  scrollToSection('news', 'click');
};

// News页面滚动事件处理
const handleNewsScroll = () => {
  if (currentSection.value === 'news') {
    updateScrollInfo();
  }
};

const handleScroll = (event) => {
  // 由于我们使用同屏切换，不再需要处理实际滚动
  // 保留函数以防其他地方调用
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

  const result = await newsStore.fetchNews(page, 12, searchQuery.value)
  if (!result.success) {
    error.value = result.error
  }
  isLoading.value = false
}

const loadMoreNews = async () => {
  if (isLoading.value || !hasMore.value) return

  isLoading.value = true
  const result = await newsStore.loadMoreNews(searchQuery.value)
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

// 认证相关方法
const openAuthModal = () => {
  showAuthModal.value = true
}

const closeAuthModal = () => {
  showAuthModal.value = false
}

const handleAuthSuccess = () => {
  showAuthModal.value = false
  // 可以在这里添加登录成功后的逻辑，比如显示欢迎消息
}

const handleLogout = () => {
  authStore.logout()
  // 可以在这里添加退出登录后的逻辑
}

const goToAdmin = () => {
  router.push('/admin/dashboard')
}

// 监听搜索词变化
watch(searchQuery, () => {
  handleSearch()
})

// 在组件挂载时检查认证状态
onMounted(async () => {
  // 检查是否从管理后台返回
  const fromAdmin = sessionStorage.getItem('fromAdmin')
  
  // 只有不是从管理后台返回时才检查认证状态
  if (!fromAdmin) {
    await authStore.checkAuthStatus()
  }
  
  windowHeight.value = window.innerHeight;

  // 检查是否从管理后台返回，如果是则跳过Logo动画
  if (fromAdmin) {
    // 清除标记
    sessionStorage.removeItem('fromAdmin')
    // 直接隐藏Logo，跳过动画
    showLogo.value = false
  } else {
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
  }

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
</script>

<style scoped>
/* 确保过渡效果的硬件加速 */
#intro, #news {
  will-change: transform, opacity;
  backface-visibility: hidden;
  transform-style: preserve-3d;
}

/* 第二屏的自定义滚动条样式 */
#news::-webkit-scrollbar {
  width: 6px;
}

#news::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

#news::-webkit-scrollbar-thumb {
  background: #cbd5e0;
  border-radius: 3px;
  transition: background 0.3s ease;
}

#news::-webkit-scrollbar-thumb:hover {
  background: #a0aec0;
}

/* 过渡遮罩层的模糊效果优化 */
.transition-mask {
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

/* 确保文本渲染的平滑性 */
.text-smooth {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}

/* 粒子画布的性能优化 */
canvas {
  will-change: auto;
}

/* 防止选中文本 */
.no-select {
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}
</style>
