# FeedNews - 现代化新闻展示平台

一个基于 Vue3 + FastAPI 的现代化响应式新闻展示平台，复现 feedmusic.com 的精致动效和交互体验。

## 🌟 项目特色

- **极致用户体验**: 复刻 feedmusic.com 的互动动效和丝滑滚动效果
- **响应式设计**: 完美适配 PC、平板、手机等多设备场景
- **现代化技术栈**: Vue3 + FastAPI + PostgreSQL + Docker
- **容器化部署**: 一键部署，开箱即用
- **完整用户系统**: 注册登录、权限管理、内容管理

## 🚀 技术栈

### 前端

- **框架**: Vue 3 (Composition API)
- **构建工具**: Vite
- **UI 框架**: Tailwind CSS
- **状态管理**: Pinia
- **路由**: Vue Router
- **HTTP 客户端**: Axios

### 后端

- **语言**: Python 3.11+
- **框架**: FastAPI
- **数据库**: PostgreSQL
- **ORM**: SQLAlchemy 2.0 (异步模式)
- **认证**: JWT + Passlib
- **数据验证**: Pydantic

### 部署

- **容器化**: Docker + Docker Compose
- **Web 服务器**: Nginx (前端静态文件)
- **数据持久化**: PostgreSQL 数据卷

## 📱 功能特性

### 🎨 前端功能

#### 第一屏 - Introduction

- **多层视差滚动背景**: 营造深度感的动态背景效果
- **文字动画**: 主标题逐字淡入，副标题滑入效果
- **鼠标跟随**: 文字阴影跟随鼠标移动
- **色彩动画**: HSL 色彩空间循环渐变

#### 第二屏 - News

- **响应式网格布局**: PC 端 3 列，平板 2 列，移动端 1 列
- **新闻卡片**: 16:9 图片比例，悬停动效
- **懒加载**: 按需加载更多新闻内容
- **搜索功能**: 支持标题和描述搜索

#### 交互体验

- **平滑页面切换**: 滚轮/触摸触发的页面切换动画
- **进度指示**: 实时显示滚动进度
- **移动端优化**: 支持手势滑动和触摸交互

### 🔧 后端功能

#### 用户系统

- **用户注册/登录**: JWT 认证，密码加密存储
- **权限管理**: 普通用户和管理员角色
- **安全防护**: 防止 SQL 注入、XSS 攻击

#### 新闻管理

- **CRUD 操作**: 创建、读取、更新、删除新闻
- **图片上传**: 支持本地存储和云存储
- **软删除**: 保留历史记录的删除机制
- **分页查询**: 高效的分页和搜索功能

#### 管理后台

- **新闻管理**: 表格展示，批量操作
- **富文本编辑**: 支持图片上传和预览
- **权限控制**: 基于角色的访问控制

## 🛠️ 快速开始

### 环境要求

- Docker 20.10+
- Docker Compose 2.0+
- Node.js 18+ (本地开发)
- Python 3.11+ (本地开发)

### 一键启动 (推荐)

```bash
# 克隆项目
git clone <repository-url>
cd feedNews/trae

# 启动开发环境
docker-compose -f docker-compose.dev.yml up
```

访问地址:

- 前端: http://localhost:3000
- 后端 API: http://localhost:8000
- API 文档: http://localhost:8000/docs

### 本地开发

#### 后端开发

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 前端开发

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 🐳 部署指南

### 生产环境部署

1. **环境变量配置**

```bash
# 复制环境变量模板
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# 编辑环境变量
vim backend/.env
vim frontend/.env
```

2. **启动生产环境**

```bash
# 构建并启动服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

3. **数据库初始化**

```bash
# 进入后端容器
docker-compose exec backend bash

# 运行数据库迁移
python -c "from app.db.init_db import init_db; init_db()"
```

### 环境变量说明

#### 后端环境变量

```env
# 数据库配置
POSTGRES_SERVER=db
POSTGRES_USER=feednews_user
POSTGRES_PASSWORD=your_strong_password
POSTGRES_DB=feednews_db

# JWT配置
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# 应用配置
PROJECT_NAME=FeedNews
API_V1_STR=/api/v1
```

#### 前端环境变量

```env
# API地址
VITE_API_BASE_URL=http://localhost:8000/api
```

## 📁 项目结构

```
feedNews/trae/
├── frontend/                 # Vue3 前端应用
│   ├── src/
│   │   ├── components/      # 可复用组件
│   │   ├── views/          # 页面组件
│   │   ├── store/          # Pinia状态管理
│   │   ├── services/       # API服务
│   │   └── router/         # 路由配置
│   ├── Dockerfile
│   └── package.json
├── backend/                  # FastAPI 后端应用
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置
│   │   ├── db/             # 数据库配置
│   │   ├── models/         # 数据模型
│   │   └── schemas/        # Pydantic模式
│   ├── Dockerfile
│   └── requirements.txt
├── doc/                      # 项目文档
│   ├── prd.md              # 产品需求文档
│   ├── backend_spec.md     # 后端技术规格
│   ├── frontend_spec.md    # 前端技术规格
│   └── deployment.md       # 部署文档
├── docker-compose.yml        # 生产环境编排
├── docker-compose.dev.yml    # 开发环境编排
└── README.md
```

## 🔗 API 文档

启动后端服务后，可以通过以下地址访问 API 文档:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 主要 API 端点

#### 认证相关

- `POST /api/auth/register` - 用户注册
- `POST /api/auth/token` - 用户登录
- `POST /api/auth/logout` - 用户登出

#### 新闻相关

- `GET /api/news/` - 获取新闻列表
- `POST /api/news/` - 创建新闻 (需认证)
- `PUT /api/news/{id}` - 更新新闻 (需认证)
- `DELETE /api/news/{id}` - 删除新闻 (需认证)

## 🎯 性能优化

### 前端优化

- **代码分割**: 路由级别的懒加载
- **图片优化**: WebP 格式 + 懒加载
- **动画优化**: 使用 transform 和 opacity 属性
- **缓存策略**: 静态资源长期缓存

### 后端优化

- **异步处理**: SQLAlchemy 异步模式
- **连接池**: 数据库连接池管理
- **缓存机制**: Redis 缓存热点数据
- **API 限流**: 防止恶意请求

## 🔒 安全特性

- **密码加密**: bcrypt 哈希加密
- **JWT 认证**: 安全的 token 机制
- **CORS 配置**: 跨域请求控制
- **输入验证**: Pydantic 数据验证
- **SQL 注入防护**: ORM 参数化查询
- **XSS 防护**: 输入内容转义

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。
