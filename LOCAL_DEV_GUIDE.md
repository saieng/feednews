# FeedNews 本地开发指南

## 当前问题说明

由于Docker Hub镜像拉取问题，前端容器构建失败。这是网络或Docker Hub服务的临时问题。以下提供多种开发方式的解决方案。

## 解决方案

### 方案1：混合开发模式（推荐）

后端使用Docker，前端本地运行，这样可以避免Node.js镜像拉取问题。

#### 1. 启动后端和数据库
```bash
# 只启动后端和数据库服务
docker-compose -f docker-compose.dev.yml up backend-dev db -d
```

#### 2. 本地运行前端
```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

访问地址：
- 前端：http://localhost:3000 （本地Vite开发服务器）
- 后端：http://localhost:8001 （Docker容器）
- 数据库：localhost:5432

### 方案2：完全本地开发

如果你有本地PostgreSQL数据库，可以完全不使用Docker。

#### 1. 安装PostgreSQL
确保本地安装了PostgreSQL，并创建数据库：
```sql
CREATE DATABASE feedNew;
CREATE USER saieng WITH PASSWORD 'yang1234';
GRANT ALL PRIVILEGES ON DATABASE feedNew TO saieng;
```

#### 2. 配置环境变量
在 `backend/.env` 文件中设置：
```env
DATABASE_URL=postgresql+asyncpg://saieng:yang1234@localhost:5432/feedNew
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
PROJECT_NAME=FeedNews
API_V1_STR=/api/v1
```

#### 3. 启动后端
```bash
cd backend

# 安装Python依赖
pip install -r requirements.txt

# 启动开发服务器
python start.py
```

#### 4. 启动前端
```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 方案3：使用本地镜像

如果网络问题解决，可以尝试重新构建：

```bash
# 清理Docker缓存
docker system prune -a -f

# 重新构建
docker-compose -f docker-compose.dev.yml build --no-cache

# 启动服务
docker-compose -f docker-compose.dev.yml up -d
```

## 开发环境配置

### 前端环境变量

创建 `frontend/.env.development`：
```env
# 后端API地址
VITE_API_BASE_URL=http://localhost:8001

# 如果使用完全本地开发
# VITE_API_BASE_URL=http://localhost:8000
```

### 热重载功能

#### 前端热重载
- Vite自动提供热重载功能
- 修改Vue组件、CSS、JS文件会立即反映在浏览器中
- 支持HMR（热模块替换）

#### 后端热重载
- 使用 `uvicorn --reload` 启动
- 修改Python文件会自动重启服务
- 保持数据库连接不中断

## 数据库管理

### 使用Docker数据库
```bash
# 连接数据库
docker-compose -f docker-compose.dev.yml exec db psql -U saieng -d feedNew

# 查看数据库日志
docker-compose -f docker-compose.dev.yml logs db
```

### 使用本地数据库
```bash
# 连接数据库
psql -U saieng -d feedNew -h localhost

# 查看表结构
\dt

# 查看用户表
SELECT * FROM users;
```

## API测试

### 使用内置文档
访问 http://localhost:8000/docs 或 http://localhost:8001/docs 查看Swagger文档

### 使用curl测试
```bash
# 健康检查
curl http://localhost:8001/health

# 注册用户
curl -X POST "http://localhost:8001/api/v1/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"username":"testuser","email":"test@example.com","password":"password123"}'

# 登录获取token
curl -X POST "http://localhost:8001/api/v1/auth/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=testuser&password=password123"
```

## 常见问题解决

### 1. 端口冲突
如果8000或8001端口被占用：
```bash
# 查看端口占用
netstat -ano | findstr :8000

# 修改docker-compose.dev.yml中的端口映射
# 例如改为 "8002:8000"
```

### 2. 数据库连接失败
检查数据库是否正常运行：
```bash
# 检查Docker数据库状态
docker-compose -f docker-compose.dev.yml ps db

# 检查本地数据库状态
pg_isready -h localhost -p 5432
```

### 3. 前端代理问题
如果前端无法访问后端API，检查 `vite.config.js` 中的代理配置：
```javascript
export default {
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8001',
        changeOrigin: true
      }
    }
  }
}
```

## 性能优化建议

1. **使用SSD硬盘**：提高文件监听和重载速度
2. **关闭不必要的杀毒软件实时监控**：避免影响文件监听
3. **使用代码编辑器的排除功能**：排除 `node_modules`、`__pycache__` 等目录
4. **定期清理依赖**：删除未使用的npm包和Python包

## 下一步

当Docker Hub网络问题解决后，可以回到完整的Docker开发环境：
```bash
docker-compose -f docker-compose.dev.yml up -d
```

这将提供最接近生产环境的开发体验。