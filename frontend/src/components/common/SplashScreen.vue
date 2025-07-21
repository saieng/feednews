<template>
  <div 
    v-if="visible" 
    class="fixed inset-0 z-50 flex items-center justify-center bg-black transition-opacity duration-500"
    :class="{ 'opacity-0': fadeOut }"
  >
    <div class="relative">
      <svg 
        class="w-32 h-32 md:w-48 md:h-48 transition-transform duration-1000 ease-in-out"
        :class="{
          'scale-110': pulseState,
          'scale-90': !pulseState
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
import { ref, onMounted, onBeforeUnmount } from 'vue';

const props = defineProps({
  duration: {
    type: Number,
    default: 5000 // 默认5秒
  }
});

const emit = defineEmits(['complete']);

const visible = ref(true);
const fadeOut = ref(false);
const pulseState = ref(true);
let pulseInterval = null;

// 处理Logo脉动动画
const startPulseAnimation = () => {
  pulseInterval = setInterval(() => {
    pulseState.value = !pulseState.value;
  }, 1000); // 每秒切换一次状态
};

// 处理淡出动画
const handleFadeOut = () => {
  fadeOut.value = true;
  
  // 等待淡出动画完成后隐藏组件并发出完成事件
  setTimeout(() => {
    visible.value = false;
    emit('complete');
  }, 500); // 与CSS过渡时间匹配
};

onMounted(() => {
  startPulseAnimation();
  
  // 设置定时器，在指定时间后开始淡出
  setTimeout(() => {
    handleFadeOut();
  }, props.duration);
});

onBeforeUnmount(() => {
  // 清除定时器
  if (pulseInterval) {
    clearInterval(pulseInterval);
  }
});
</script>