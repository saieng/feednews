<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black">
    <!-- Logo动画 -->
    <div 
      class="relative transition-opacity duration-500"
      :class="{ 'opacity-0': logoFadeOut }"
    >
      <svg 
        class="w-32 h-32 md:w-48 md:h-48 transition-transform duration-1000 ease-in-out"
        :class="{
          'scale-125': logoScale,
          'scale-75': !logoScale
        }"
        viewBox="0 0 165.774 197.826"
      >
        <g>
          <path 
            fill="#ffffff" 
            d="M158.903,94.998L24.541,2.75c-7.14-4.9-16.889-3.07-21.789,4.046c-4.899,7.137-3.078,16.895,4.05,21.798
            l112.648,77.838l-90.363,49.234v-47.938h24.581L1.335,39.564v50.134v19.201v73.252c0,5.54,1.857,10.669,6.637,13.49
            c2.461,1.459,4.688,2.185,7.441,2.185c2.593,0,4.935-0.643,7.288-1.941l135.008-74.232c4.774-2.621,7.768-7.521,8.047-12.959
            C166.019,103.271,163.386,98.082,158.903,94.998"
          />
        </g>
      </svg>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const logoScale = ref(true)
const logoFadeOut = ref(false)
let logoInterval = null

onMounted(() => {
  // 启动logo动画
  logoInterval = setInterval(() => {
    logoScale.value = !logoScale.value
  }, 1000) // 每秒切换一次缩放状态
  
  // 5秒后开始淡出logo
  setTimeout(() => {
    logoFadeOut.value = true
    
    // 淡出动画完成后跳转到主页
    setTimeout(() => {
      clearInterval(logoInterval)
      router.push('/home')
    }, 500)
  }, 5000)
})
</script>