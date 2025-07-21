# FeedNews 前端项目

基于 Vue 3 + Vite + Tailwind CSS 构建的现代化新闻管理系统。

## 技术栈

- **Vue 3** - 渐进式 JavaScript 框架
- **Vite** - 下一代前端构建工具
- **Tailwind CSS** - 实用优先的 CSS 框架
- **Pinia** - Vue 的状态管理库
- **Vue Router** - Vue.js 的官方路由
- **Axios** - HTTP 客户端

## 项目结构

```
frontend/
├── public/                 # 静态资源
├── src/
│   ├── assets/            # 资源文件
│   │   └── main.css       # 主样式文件
│   ├── components/        # 可复用组件
│   │   ├── common/        # 通用组件
│   │   └── news/          # 新闻相关组件
│   ├── services/          # API 服务
│   ├── store/             # 状态管理
│   ├── views/             # 页面组件
│   │   ├── admin/         # 管理后台页面
│   │   └── HomeView.vue   # 主页
│   ├── router/            # 路由配置
│   ├── App.vue            # 根组件
│   └── main.js            # 入口文件
├── package.json           # 项目配置
├── vite.config.js         # Vite 配置
├── tailwind.config.js     # Tailwind 配置
└── README.md             # 项目说明
```

## 功能特性

### 用户端功能
- 📰 新闻列表展示
- 🔍 新闻搜索
- 📱 响应式设计
- ⚡ 快速加载

### 管理端功能
- 🔐 用户认证
- ✍️ 新闻创建/编辑/删除
- 📊 管理后台仪表盘
- 🖼️ 图片上传

## 快速开始

### 安装依赖

```bash
npm install
```

### 开发环境

```bash
npm run dev
```

访问 http://localhost:5173 查看应用。

### 构建生产版本

```bash
npm run build
```

### 代码检查

```bash
npm run lint
```

## 环境变量

创建 `.env` 文件：

```
VITE_API_URL=http://localhost:3000/api
```

## API 接口

项目使用以下 API 端点：

- **认证**
  - POST `/auth/login` - 用户登录
  - POST `/auth/register` - 用户注册
  - GET `/auth/profile` - 获取用户信息

- **新闻**
  - GET `/news` - 获取新闻列表
  - GET `/news/:id` - 获取单条新闻
  - POST `/news` - 创建新闻
  - PUT `/news/:id` - 更新新闻
  - DELETE `/news/:id` - 删除新闻
  - POST `/news/upload-image` - 上传图片

## 组件说明

### 通用组件
- `LoadingSpinner.vue` - 加载动画
- `ErrorMessage.vue` - 错误提示

### 新闻组件
- `NewsCard.vue` - 新闻卡片
- `NewsGrid.vue` - 新闻网格列表

### 认证组件
- `AuthModal.vue` - 认证模态框

## 路由说明

- `/` - 主页
- `/admin/dashboard` - 管理后台
- `/admin/news/create` - 创建新闻
- `/admin/news/edit/:id` - 编辑新闻

## 状态管理

### Auth Store
管理用户认证状态：
- `token` - 用户令牌
- `user` - 用户信息
- `isAuthenticated` - 认证状态

### News Store
管理新闻数据：
- `newsList` - 新闻列表
- `currentNews` - 当前新闻
- `pagination` - 分页信息

## 开发规范

- 使用 Composition API
- 遵循 ESLint 配置
- 使用 Tailwind CSS 类名
- 组件命名采用 PascalCase
- 文件命名采用 kebab-case

## 部署

### Docker 部署

```bash
docker build -t feednews-frontend .
docker run -p 80:80 feednews-frontend
```

### 静态文件部署

构建后的文件位于 `dist/` 目录，可直接部署到任何静态文件服务器。

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送分支
5. 创建 Pull Request

## 许可证

MIT License