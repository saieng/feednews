# FeedNews Backend

基于 FastAPI 的现代化新闻管理系统后端服务。

## 技术栈

- **Python 3.11+**
- **FastAPI** - 现代化的 Web 框架
- **SQLAlchemy 2.0** - 异步 ORM
- **PostgreSQL** - 数据库
- **Pydantic** - 数据验证
- **JWT** - 身份认证
- **Docker** - 容器化部署

## 项目结构

```
app/
├── api/                    # API 路由
│   ├── v1/
│   │   ├── endpoints/      # API 端点
│   │   │   ├── auth.py     # 认证相关
│   │   │   ├── news.py     # 新闻管理
│   │   │   └── admin.py    # 管理后台
│   │   └── api.py          # 路由聚合
│   └── deps.py             # 依赖注入
├── core/                   # 核心配置
│   ├── config.py           # 应用配置
│   └── security.py         # 安全相关
├── db/                     # 数据库
│   ├── base.py             # 基础模型
│   ├── session.py          # 会话管理
│   └── init_db.py          # 数据库初始化
├── models/                 # 数据模型
│   ├── user.py             # 用户模型
│   └── news.py             # 新闻模型
├── schemas/                # Pydantic 模式
│   ├── user.py             # 用户模式
│   ├── news.py             # 新闻模式
│   └── token.py            # 令牌模式
└── main.py                 # 应用入口
```

## 快速开始

### 1. 环境准备

```bash
# 复制环境变量文件
cp .env.example .env

# 编辑环境变量（根据需要修改数据库连接信息和密钥）
# 特别注意修改 SECRET_KEY，可以使用以下命令生成：
# openssl rand -hex 32
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动服务

```bash
# 方式1：使用 uvicorn 直接启动
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 方式2：使用启动脚本
python start.py
```

### 4. 使用 Docker 启动

```bash
# 构建镜像
docker build -t feednews-backend .

# 运行容器（需要先启动 PostgreSQL）
docker run -p 8000:8000 --env-file .env feednews-backend
```

## API 文档

启动服务后，可以访问以下地址查看 API 文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

## 主要功能

### 认证系统

- **用户注册**: `POST /api/v1/auth/register`
- **用户登录**: `POST /api/v1/auth/token`
- **JWT 令牌认证**

### 新闻管理

- **获取新闻列表**: `GET /api/v1/news/` (公开)
- **创建新闻**: `POST /api/v1/news/` (需要认证)
- **更新新闻**: `PUT /api/v1/news/{id}` (需要所有权)
- **删除新闻**: `DELETE /api/v1/news/{id}` (软删除)

### 管理后台

- **管理员新闻列表**: `GET /api/v1/admin/news`
- **强制删除新闻**: `DELETE /api/v1/admin/news/{id}/force`
- **恢复已删除新闻**: `POST /api/v1/admin/news/{id}/restore`
- **用户列表**: `GET /api/v1/admin/users`

## 默认账户

系统启动时会自动创建默认管理员账户：

- **用户名**: `admin`
- **密码**: `admin123`
- **邮箱**: `admin@feednews.com`

**注意**: 生产环境中请立即修改默认密码！

## 数据库

### 自动初始化

应用启动时会自动：
1. 创建所有数据表
2. 创建默认管理员用户
3. 插入示例新闻数据

### 数据库迁移

如果需要手动管理数据库迁移，可以使用 Alembic：

```bash
# 初始化迁移
alembic init alembic

# 生成迁移文件
alembic revision --autogenerate -m "Initial migration"

# 执行迁移
alembic upgrade head
```

## 开发指南

### 添加新的 API 端点

1. 在 `app/api/v1/endpoints/` 中创建新的路由文件
2. 在 `app/api/v1/api.py` 中注册路由
3. 如需要，在 `app/schemas/` 中添加相应的 Pydantic 模式

### 添加新的数据模型

1. 在 `app/models/` 中创建新的模型文件
2. 在 `app/db/base.py` 中导入新模型
3. 在 `app/schemas/` 中创建对应的 Pydantic 模式

## 部署

推荐使用 Docker Compose 进行部署，详见项目根目录的 `docker-compose.yml` 文件。

## 安全注意事项

1. **修改默认密钥**: 生产环境中必须修改 `SECRET_KEY`
2. **修改默认密码**: 修改默认管理员账户密码
3. **CORS 配置**: 生产环境中应限制 CORS 允许的域名
4. **HTTPS**: 生产环境中应使用 HTTPS
5. **环境变量**: 敏感信息不要提交到版本控制系统

## 许可证

MIT License