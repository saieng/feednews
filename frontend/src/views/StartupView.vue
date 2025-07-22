<template>
  <div class="fixed inset-0 bg-black flex items-center justify-center z-50">
    <transition name="logo-fade">
      <img v-if="showLogo" src="@/assets/logo.svg" alt="Logo" class="w-48 h-48 transition-transform duration-1000" :class="logoScaleClass" />
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const showLogo = ref(true);
const logoScaleClass = ref('scale-100');
let scaleInterval = null;

onMounted(() => {
  scaleInterval = setInterval(() => {
    logoScaleClass.value = logoScaleClass.value === 'scale-100' ? 'scale-110' : 'scale-100';
  }, 1000);

  setTimeout(() => {
    showLogo.value = false;
    setTimeout(() => {
      router.push('/home');
    }, 800); // Wait for fade-out transition
  }, 4000); // Logo display time
});

onBeforeUnmount(() => {
  clearInterval(scaleInterval);
});
</script>

<style scoped>
.logo-fade-enter-active, .logo-fade-leave-active {
  transition: opacity 0.8s ease-in-out;
}
.logo-fade-enter-from, .logo-fade-leave-to {
  opacity: 0;
}
</style>