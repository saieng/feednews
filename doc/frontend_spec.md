# FeedNews 前端技术设计文档

## 1. 概述

本文档旨在为 FeedNews 项目的前端开发提供清晰、统一的技术规范和架构指导。基于产品需求文档 (PRD)，本文档将详细阐述技术选型、项目结构、组件设计、状态管理方案及路由规划。

## 2. 技术栈

为确保开发效率、性能和可维护性，前端将采用以下技术栈：

- **框架**: Vue 3 (使用 Composition API)
- **构建工具**: Vite
- **状态管理**: Pinia
- **UI 框架**: Tailwind CSS
- **HTTP客户端**: Axios
- **路由**: Vue Router

## 3. 项目结构

采用模块化、功能明确的目录结构，便于团队协作和长期维护。

```
src/
├── assets/         # 静态资源 (图片, 字体, 全局样式)
├── components/     # 全局可复用组件
│   ├── common/     # 基础组件 (按钮, 输入框等)
│   ├── layout/     # 布局组件 (TheNavbar, AppProgressBar)
│   └── news/       # 新闻相关组件 (NewsCard)
│   └── auth/       # 认证相关组件 (AuthModal)
├── views/          # 页面级组件 (视图)
│   ├── IntroductionView.vue
│   ├── NewsView.vue
│   └── admin/
│       └── Dashboard.vue
├── router/         # 路由配置
│   └── index.js
├── store/          # Pinia 状态管理
│   ├── auth.js     # 认证状态
│   └── news.js     # 新闻数据状态
├── services/       # API 请求服务
│   ├── apiClient.js # Axios 实例和拦截器配置
│   └── newsService.js
│   └── authService.js
├── utils/          # 工具函数
└── main.js         # 应用入口文件
```

## 4. 组件拆解

将 UI 界面拆分为一系列高内聚、低耦合的可复用组件。

### 4.1 `TheNavbar.vue`

- **描述**: 应用的顶部导航栏，固定在页面顶部。
- **Props**:
  - `isLoggedIn` (Boolean): 标识用户是否登录。
  - `username` (String): 当前登录的用户名。
- **Events**:
  - `@scrollTo(section: 'introduction' | 'news')`: 触发滚动到指定区域。
  - `@openAuthModal`: 打开登录/注册模态框。
  - `@logout`: 触发用户登出操作。

### 4.2 AppProgressBar.vue
- 滚动进度条，使用 transform: scaleX() 实现宽度动画，200ms ease-out 过渡。
- 进度计算：scrollTop / (totalHeight - viewportHeight) * 100%。

### 4.3 IntroductionView.vue
- 多层视差背景：三层背景元素，分别绑定不同的滚动系数（0.3x/0.7x/1.2x），通过 requestAnimationFrame 优化。
- 色彩动画：HSL 色彩渐变，30s 循环。
- 粒子/几何浮动：Canvas/WebGL 或 CSS 动画实现。
- 文字动画：主标题逐字淡入，副标题滑入，滚动时透明度和位置动态变化。
- 鼠标跟随：监听 mousemove，动态调整文字阴影。

### 4.4 `NewsView.vue`

- **描述**: 应用的第二屏，以网格布局展示新闻卡片列表。
- **Props**:
  - `newsItems` (Array): 新闻数据列表。
- **Events**:
  - `@loadMore`: 点击“加载更多”时触发。

### 4.5 `NewsCard.vue`

- **描述**: 单个新闻的卡片展示组件。
- **Props**:
  - `news` (Object): 新闻对象，包含 `title`, `description`, `imageUrl`, `creator` 等字段。
- **Events**:
  - `@cardClick(newsId: number)`: 点击卡片时触发，用于页面跳转。

### 4.6 AuthModal.vue
- 登录/注册切换，表单实时校验。
- 密码安全输入，错误提示。
- 认证成功后自动关闭并刷新用户状态。

### 4.7 页面切换与滚动交互
- 滚轮/触摸监听：滚动超过 40%/50% 视口高度自动切换屏幕。
- 滚动方向检测，300ms 防抖。
- 动画：CSS transform: translateY()，will-change: transform 硬件加速。
- 边界检测与回弹动画。
- 移动端支持左右滑动切换，模拟惯性滚动。

## 5. 响应式设计与性能优化

- Tailwind 配置断点：<640px、640-768px、768-1024px、1024-1280px、>1280px。
- 字体：clamp() 实现平滑缩放。
- 图片：srcset 多分辨率，IntersectionObserver 懒加载。
- 首屏加载优先级，代码分割（Vite 动态 import），CDN 加速。
- 滚动/动画仅用 transform/opacity，避免 layout thrash。
- 滚动事件节流（16ms），离屏元素暂停渲染。
- 电池优化：监听 Battery API，低电量时关闭高复杂度动画。

### 5.1 响应式交互细节
- 视口尺寸变化监听，动态调整布局和字体大小。
- 触摸事件支持，移动端滑动切换页面。
- 页面切换动画使用 CSS transition 和 Vue 过渡钩子，确保流畅体验。
- 导航栏根据滚动位置高亮当前菜单项。
- 滚动进度条实时更新，使用 requestAnimationFrame 优化性能。

### 5.2 首页背景动效实现
- 多层视差背景通过绑定不同滚动速度实现深度感。
- 色彩动画使用 CSS HSL 变量和动画循环。
- 粒子和几何浮动采用 Canvas API，结合 requestAnimationFrame 实现高性能动画。
- 鼠标跟随效果监听 mousemove，动态调整文字阴影和背景元素位置。

### 5.3 前端安全措施
- 所有 API 请求均使用 HTTPS。
- Axios 请求拦截器统一处理 token，防止 CSRF。
- 输入表单使用严格校验，防止 XSS 注入。
- 认证状态存储在 Pinia，避免 localStorage 直接暴露敏感信息。
- 路由守卫保护后台管理页面，未登录用户重定向登录页。

### 5.4 性能要求
- 代码分割，按需加载路由组件。
- 图片懒加载，减少首屏加载时间。
- 使用 Vite 进行构建优化，开启缓存和压缩。
- 避免不必要的响应式数据，减少渲染开销。
- 使用 Web Worker 处理复杂计算（如粒子动画）以避免主线程阻塞。

## 6. 状态管理 (Pinia)

使用 Pinia 进行全局状态管理，确保数据流的清晰和可预测性。

### 5.1 `authStore`

- **State**:
  - `token` (String | null): 存储用户的 JWT。
  - `user` (Object | null): 存储用户信息 (如 username, id)。
  - `isLoggedIn` (Boolean): 计算属性，根据 `token` 判断。
- **Actions**:
  - `login(credentials)`: 处理登录逻辑，获取并存储 token 和 user。
  - `register(userInfo)`: 处理注册逻辑。
  - `logout()`: 清除 token 和用户信息。
  - `checkAuthStatus()`: 应用加载时检查本地存储的 token。

### 5.2 `newsStore`

- **State**:
  - `newsList` (Array): 存储新闻列表。
  - `currentPage` (Number): 当前分页页码。
  - `totalNews` (Number): 新闻总数。
  - `isLoading` (Boolean): 标识是否正在加载新闻。
- **Actions**:
  - `fetchNews(page: number, limit: number)`: 从后端获取新闻列表。
  - `loadMoreNews()`: 加载下一页新闻并追加到 `newsList`。

## 6. 路由 (Vue Router)

虽然主页是单页滚动体验，但后台管理功能需要独立的路由。

- `/`: 主页，包含 `IntroductionView` 和 `NewsView`。
- `/admin/dashboard`: 新闻管理后台页面。
- `/admin/news/create`: 创建新闻页面。
- `/admin/news/edit/:id`: 编辑新闻页面。

路由守卫将用于保护后台管理路由，只有认证用户才能访问。