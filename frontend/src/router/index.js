import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue'),
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: () => import('@/views/admin/Dashboard.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/admin/news/create',
    name: 'CreateNews',
    component: () => import('@/views/admin/CreateNews.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/admin/news/edit/:id',
    name: 'EditNews',
    component: () => import('@/views/admin/EditNews.vue'),
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  },
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // 检查是否从管理后台返回首页
  const fromAdmin = sessionStorage.getItem('fromAdmin')
  
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    // 如果是从管理后台返回首页，清除标记但不重定向
    if (fromAdmin && to.path === '/') {
      sessionStorage.removeItem('fromAdmin')
      next()
    } else {
      next('/')
    }
  } else {
    next()
  }
})

export default router