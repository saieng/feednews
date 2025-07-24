# FeedNews Docker 部署指南

## 问题解决

### 原始错误分析
错误信息显示 `nginx:stable-alpine` 镜像拉取失败，主要原因：
1. 缺少 `nginx.conf` 配置文件
2. Docker Compose 配置中数据库连接字符串拼写错误（`stgresql` 应为 `postgresql`）
3. 数据库服务名配置错误（应使用 `db` 而不是 `localhost`）

### 已修复的问题
✅ 创建了 `frontend/nginx.conf` 配置文件  
✅ 修复了数据库连接字符串拼写错误  
✅ 修正了服务间网络连接配置  
✅ 添加了开发环境支持，实现代码热重载  

## 部署方式

### 1. 生产环境部署
```bash
# 构建并启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

访问地址：
- 前端：http://localhost
- 后端API：http://localhost:8000
- API文档：http://localhost:8000/docs

### 2. 开发环境部署（推荐）
```bash
# 使用开发环境配置启动
docker-compose -f docker-compose.dev.yml up -d

# 或者使用profiles方式
docker-compose --profile dev up -d
```

访问地址：
- 前端开发服务器：http://localhost:3000 （支持热重载）
- 后端开发服务器：http://localhost:8001 （支持热重载）
- 数据库：localhost:5432

### 3. 开发环境特性

#### 前端热重载
- 代码修改后自动刷新浏览器
- 支持Vue组件热替换
- 实时CSS更新

#### 后端热重载
- Python代码修改后自动重启服务
- 保持数据库连接
- 实时API更新

#### 数据库持久化
- 开发和生产环境使用不同的数据卷
- 数据在容器重启后保持

## 常用命令

### 服务管理
```bash
# 停止所有服务
docker-compose down

# 停止并删除数据卷
docker-compose down -v

# 重新构建镜像
docker-compose build

# 强制重新构建
docker-compose build --no-cache
```

### 开发调试
```bash
# 查看特定服务日志
docker-compose logs -f backend-dev
docker-compose logs -f frontend-dev

# 进入容器调试
docker-compose exec backend-dev bash
docker-compose exec frontend-dev sh

# 重启特定服务
docker-compose restart backend-dev
```

### 数据库管理
```bash
# 连接数据库
docker-compose exec db psql -U saieng -d feedNew

# 备份数据库
docker-compose exec db pg_dump -U saieng feedNew > backup.sql

# 恢复数据库
docker-compose exec -T db psql -U saieng feedNew < backup.sql
```

## 环境变量配置

### 后端环境变量
- `POSTGRES_SERVER`: 数据库服务器地址
- `DATABASE_URL`: 完整数据库连接字符串
- `SECRET_KEY`: JWT密钥
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token过期时间

### 前端环境变量
- `VITE_API_BASE_URL`: 后端API地址
- `CHOKIDAR_USEPOLLING`: 启用文件监听轮询

## 性能优化建议

### 开发环境
1. 使用 `.dockerignore` 文件排除不必要的文件
2. 合理配置数据卷映射，避免映射大型目录
3. 定期清理未使用的镜像和容器

### 生产环境
1. 使用多阶段构建减小镜像体积
2. 启用Nginx gzip压缩
3. 配置适当的缓存策略
4. 使用健康检查确保服务可用性

## 故障排除

### 常见问题
1. **端口冲突**：修改docker-compose.yml中的端口映射
2. **权限问题**：确保Docker有足够权限访问项目目录
3. **网络问题**：检查防火墙设置和Docker网络配置
4. **镜像拉取失败**：尝试更换Docker镜像源

### 日志分析
```bash
# 查看详细启动日志
docker-compose up --no-deps --build backend-dev

# 查看容器资源使用情况
docker stats
```