# FeedNews 部署文档

## 1. 概述

本文档提供了部署 FeedNews 项目所需的所有信息，包括系统架构、环境变量配置和容器化部署指南。我们的目标是实现一个可重复、一致且易于管理的部署流程。

## 2. 部署架构

系统采用基于容器的多服务架构，由以下三个核心组件构成：

- **`frontend`**: 一个 Nginx 服务器，用于托管编译后的 Vue.js 单页应用 (SPA) 的静态文件。
- **`backend`**: FastAPI 应用服务，处理所有业务逻辑和 API 请求。
- **`db`**: 一个 PostgreSQL 数据库实例，用于持久化存储所有数据。

这三个服务将被编排在同一个 Docker 网络中，以便它们可以相互通信。

## 3. 环境变量配置

为了保证配置的灵活性和安全性，项目严重依赖环境变量。在部署或本地开发前，需要创建 `.env` 文件。

以下是前后端服务所需的环境变量列表。

### 3.1 后端 (`backend`) 环境变量

创建一个 `.env` 文件，并放置在后端项目的根目录下。

**.env.example (for backend)**

```env
# PostgreSQL 数据库连接信息
POSTGRES_SERVER=db
POSTGRES_USER=feednews_user
POSTGRES_PASSWORD=a_very_strong_password
POSTGRES_DB=feednews_db
DATABASE_URL=postgresql+asyncpg://feednews_user:a_very_strong_password@db:5432/feednews_db

# JWT Token 安全配置
# 使用 `openssl rand -hex 32` 生成一个随机密钥
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440 # 24 hours

# 应用配置
PROJECT_NAME=FeedNews
API_V1_STR=/api/v1
```

### 3.2 前端 (`frontend`) 环境变量

前端应用在构建时需要知道后端 API 的地址。

**.env.example (for frontend)**

```env
# 后端 API 的基础 URL
VITE_API_BASE_URL=http://localhost:8000/api
```

**注意**: 在生产环境中，`VITE_API_BASE_URL` 应指向后端服务的公共访问地址。

## 4. Docker 编排

我们将使用 `docker-compose.yml` 文件来定义和管理上述三个服务。该文件将负责：

- 构建 `frontend` 和 `backend` 服务的 Docker 镜像。
- 拉取官方的 `postgres` 镜像。
- 配置服务间的网络和依赖关系。
- 挂载卷以实现数据持久化（数据库）和代码热重载（开发环境）。
- 将环境变量从 `.env` 文件注入到相应的服务中。

完整的 `docker-compose.yml` 文件示例如下：

```yaml
version: "3.8"

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - feednews-network

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - POSTGRES_SERVER=db
      - POSTGRES_USER=feednews_user
      - POSTGRES_PASSWORD=a_very_strong_password
      - POSTGRES_DB=feednews_db
      - DATABASE_URL=postgresql+asyncpg://feednews_user:a_very_strong_password@db:5432/feednews_db
      - SECRET_KEY=your_super_secret_key_here
      - ALGORITHM=HS256
      - ACCESS_TOKEN_EXPIRE_MINUTES=1440
      - PROJECT_NAME=FeedNews
      - API_V1_STR=/api/v1
    depends_on:
      - db
    networks:
      - feednews-network

  db:
    image: postgres:15
    restart: always
    environment:
      POSTGRES_USER: feednews_user
      POSTGRES_PASSWORD: a_very_strong_password
      POSTGRES_DB: feednews_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - feednews-network

networks:
  feednews-network:
    driver: bridge

volumes:
  postgres_data:
```

## 5. 部署步骤

### 5.1 服务器准备

- 选择支持 Docker 的服务器环境（如 Ubuntu 20.04+，CentOS 7+，Windows Server 2019+）。
- 安装 Docker 和 Docker Compose。

### 5.2 数据库初始化

- PostgreSQL 数据库由 Docker Compose 自动启动并初始化。
- 确保环境变量配置正确，数据库用户和密码安全。

### 5.3 安装依赖

- 前端依赖在 Docker 构建阶段自动安装。
- 后端依赖通过 `requirements.txt` 在 Docker 构建阶段安装。

### 5.4 构建与启动服务

```bash
# 在项目根目录执行

docker-compose build

docker-compose up -d
```

- 访问 http://服务器 IP/ 查看前端页面。
- 后端 API 监听在 8000 端口。

### 5.5 MCP 测试服务器搭建

- MCP 测试服务器为内部测试环境，建议使用与生产环境相同的 Docker Compose 配置。
- 可配置独立的环境变量文件 `.env.mcp`，并在启动时指定：

```bash
docker-compose --env-file .env.mcp up -d
```

- 通过测试服务器验证功能和性能，确保发布质量。

---
