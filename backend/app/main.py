from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化数据库
    await init_db()
    yield
    # 关闭时的清理工作（如果需要）


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# 设置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含API路由
app.include_router(api_router, prefix=settings.API_V1_STR)

# 挂载静态文件服务
# 使用相对路径，适配Docker容器环境
upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")

print(f"静态文件服务 - 计算的上传目录路径: {upload_dir}")

# 确保上传目录存在
os.makedirs(upload_dir, exist_ok=True)

# 挂载静态文件
app.mount("/uploads", StaticFiles(directory=upload_dir), name="uploads")


@app.get("/")
async def root():
    """根路径"""
    return {"message": "Welcome to FeedNews API"}


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}