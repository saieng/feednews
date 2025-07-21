# FeedNews 后端技术设计文档

## 1. 概述

本文档为 FeedNews 项目的后端服务提供技术实现蓝图。内容涵盖技术栈选型、数据库设计、API 规范和项目代码结构，旨在确保后端服务的健壮性、可扩展性和安全性。

## 2. 技术栈

- **语言**: Python 3.11+
- **框架**: FastAPI
- **数据库**: PostgreSQL
- **ORM**: SQLAlchemy 2.0 (异步模式)
- **数据验证**: Pydantic
- **安全与认证**: Passlib (用于密码哈希), python-jose (用于JWT)

## 3. 数据库 Schema (SQL DDL)

数据库包含 `users` 和 `news` 两个核心表。

```sql
-- 用户表 (users)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 新闻表 (news)
CREATE TABLE news (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description VARCHAR(500) NOT NULL,
    image_url VARCHAR(255),
    creator_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE -- 用于软删除
);

-- 为 updated_at 创建自动更新触发器
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = NOW();
   RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
CREATE TRIGGER update_news_updated_at BEFORE UPDATE ON news FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
```

## 4. API 规范 (OpenAPI 3.0.0 YAML)

API 遵循 RESTful 设计原则，使用 OpenAPI 3.0.0 规范进行定义。

```yaml
openapi: 3.0.0
info:
  title: FeedNews API
  version: 1.0.0
  description: FeedNews 项目的后端 API 规范

paths:
  /api/auth/register:
    post:
      summary: 用户注册
      tags:
        - Auth
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                  example: newuser
                email:
                  type: string
                  format: email
                  example: user@example.com
                password:
                  type: string
                  format: password
                  example: StrongPassword123
      responses:
        '201':
          description: 用户创建成功
        '400':
          description: 无效的输入

  /api/auth/token:
    post:
      summary: 用户登录获取 Token
      tags:
        - Auth
      requestBody:
        required: true
        content:
          application/x-www-form-urlencoded:
            schema:
              type: object
              properties:
                username:
                  type: string
                  description: "用户名或邮箱"
                password:
                  type: string
      responses:
        '200':
          description: 登录成功，返回 access token
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
                  token_type:
                    type: string
                    example: bearer
        '401':
          description: 认证失败

  /api/news/:
    get:
      summary: 获取新闻列表 (公开)
      tags:
        - News
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 10
        - name: q
          in: query
          schema:
            type: string
          description: "搜索关键词"
      responses:
        '200':
          description: 成功返回新闻列表

    post:
      summary: 创建新新闻 (需要认证)
      tags:
        - News
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/NewsCreate'
      responses:
        '201':
          description: 新闻创建成功

  /api/news/{id}:
    put:
      summary: 更新新闻 (需要认证和所有权)
      tags:
        - News
      security:
        - bearerAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/NewsUpdate'
      responses:
        '200':
          description: 更新成功
        '403':
          description: 无权限操作
        '404':
          description: 新闻未找到

    delete:
      summary: 删除新闻 (需要认证和所有权)
      tags:
        - News
      security:
        - bearerAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '204':
          description: 删除成功
        '403':
          description: 无权限操作
        '404':
          description: 新闻未找到

components:
  schemas:
    NewsCreate:
      type: object
      properties:
        title:
          type: string
          maxLength: 100
        description:
          type: string
          maxLength: 500
        image_url:
          type: string
          format: uri
    NewsUpdate:
      type: object
      properties:
        title:
          type: string
          maxLength: 100
        description:
          type: string
          maxLength: 500
        image_url:
          type: string
          format: uri

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```
## 5. 项目结构

```
app/
├── api/
│   ├── __init__.py
│   └── v1/
│       ├── __init__.py
│       ├── endpoints/
│       │   ├── __init__.py
│       │   ├── auth.py
│       │   ├── news.py
│       │   └── admin.py       # 管理后台相关接口
│       └── api.py      # 组合所有 v1 路由
├── core/
│   ├── __init__.py
│   ├── config.py     # 环境变量和配置
│   └── security.py   # 密码哈希, JWT
├── db/
│   ├── __init__.py
│   ├── base.py       # DeclarativeBase 和基础模型
│   └── session.py    # 数据库会话管理
├── models/
│   ├── __init__.py
│   ├── news.py
│   └── user.py
├── schemas/
│   ├── __init__.py
│   ├── news.py
│   ├── token.py
│   ├── user.py
│   └── admin.py       # 管理后台相关数据模型
└── main.py           # FastAPI 应用实例
```

## 6. 管理后台功能设计

### 6.1 登录页面
- 使用 Vue3 + TailwindCSS 实现简洁响应式登录表单
- 表单包含用户名、密码、记住我复选框
- 实时表单验证，错误提示友好
- 登录成功后存储 JWT，跳转后台首页

### 6.2 新闻管理列表
- 表格展示新闻标题、创建者、创建时间、操作按钮（编辑、删除）
- 支持分页，每页显示 10 条新闻，显示总页数
- 搜索框支持按标题模糊搜索
- 批量删除功能，管理员权限可用
- 排序功能，支持按创建时间和标题排序

### 6.3 新闻编辑表单
- 富文本编辑器支持标题和描述编辑
- 图片上传支持拖拽和预览
- 实时保存草稿，防止数据丢失
- 表单验证，提示必填项和格式错误

### 6.4 后端接口设计
- 新增 `admin.py` 路由文件，提供管理后台相关接口
- 接口包括新闻列表查询、新闻创建、编辑、删除，支持权限校验
- 使用 JWT 认证，确保接口安全

### 6.5 前端路由设计
- `/admin/login` 登录页
- `/admin/dashboard` 新闻管理列表页
- `/admin/news/create` 新建新闻页
- `/admin/news/edit/:id` 编辑新闻页

### 6.6 安全与权限
- 路由守卫保护后台路由，未登录用户重定向登录页
- 后端接口权限校验，确保只有管理员或新闻创建者可操作

### 6.7 性能优化
- 代码分割，按需加载后台页面组件
- 使用缓存减少接口请求次数
- 图片懒加载，提升列表渲染性能

