<template>
  <div 
    class="touch-handler"
    @touchstart="handleTouchStart"
    @touchmove="handleTouchMove"
    @touchend="handleTouchEnd"
  >
    <slot></slot>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  threshold: {
    type: Number,
    default: 50 // 触发滑动事件的最小距离
  },
  vertical: {
    type: Boolean,
    default: true // 默认垂直方向
  }
});

const emit = defineEmits(['swipeUp', 'swipeDown', 'swipeLeft', 'swipeRight']);

const touchStartY = ref(0);
const touchStartX = ref(0);

const handleTouchStart = (event) => {
  touchStartY.value = event.touches[0].clientY;
  touchStartX.value = event.touches[0].clientX;
};

const handleTouchMove = (event) => {
  // 可以在这里添加阻止默认行为，防止页面滚动
  // 但这可能会影响其他触摸交互，谨慎使用
  // event.preventDefault();
};

const handleTouchEnd = (event) => {
  const touchEndY = event.changedTouches[0].clientY;
  const touchEndX = event.changedTouches[0].clientX;
  
  const deltaY = touchStartY.value - touchEndY;
  const deltaX = touchStartX.value - touchEndX;
  
  // 判断是垂直滑动还是水平滑动
  if (props.vertical && Math.abs(deltaY) > Math.abs(deltaX)) {
    // 垂直滑动
    if (Math.abs(deltaY) >= props.threshold) {
      if (deltaY > 0) {
        emit('swipeUp', { deltaY, deltaX });
      } else {
        emit('swipeDown', { deltaY, deltaX });
      }
    }
  } else if (!props.vertical && Math.abs(deltaX) > Math.abs(deltaY)) {
    // 水平滑动
    if (Math.abs(deltaX) >= props.threshold) {
      if (deltaX > 0) {
        emit('swipeLeft', { deltaY, deltaX });
      } else {
        emit('swipeRight', { deltaY, deltaX });
      }
    }
  }
};
</script>

<style scoped>
.touch-handler {
  width: 100%;
  height: 100%;
  touch-action: pan-y; /* 允许垂直平移，但阻止水平平移 */
}
</style>