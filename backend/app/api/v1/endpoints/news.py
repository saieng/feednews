from typing import Any, Optional
from math import ceil
import logging
import os
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload

from app.api import deps
from app.db.session import get_db
from app.models.news import News
from app.models.user import User
from app.schemas.news import (
    News as NewsSchema,
    NewsCreate,
    NewsUpdate,
    NewsListResponse
)
from app.core.config import settings

# 设置日志
logger = logging.getLogger(__name__)

router = APIRouter()


def get_full_image_url(image_url: Optional[str]) -> Optional[str]:
    """获取完整的图片URL"""
    if not image_url:
        logger.debug("图片URL为空，返回None")
        return None
    
    # 如果已经是完整URL，直接返回
    if image_url.startswith(('http://', 'https://')):
        logger.debug(f"图片URL已是完整路径: {image_url}")
        return image_url
    
    # 拼接完整URL
    full_url = f"{settings.SERVER_HOST}/{settings.UPLOAD_DIR}/{image_url.lstrip('/')}"
    logger.debug(f"拼接图片URL: {image_url} -> {full_url}")
    return full_url


@router.get("/", response_model=NewsListResponse)
async def read_news(
    db: AsyncSession = Depends(get_db),
    page: int = Query(default=1, ge=1, description="页码"),
    limit: int = Query(default=10, ge=1, le=100, description="每页数量"),
    q: Optional[str] = Query(default=None, description="搜索关键词")
) -> Any:
    """获取新闻列表（公开接口）"""
    logger.info(f"=== 新闻列表查询开始 ===")
    logger.info(f"查询参数: page={page}, limit={limit}, q={q}")
    
    # 构建查询条件
    query = select(News).where(News.deleted_at.is_(None))
    
    # 添加搜索条件
    if q:
        search_filter = or_(
            News.title.ilike(f"%{q}%"),
            News.description.ilike(f"%{q}%")
        )
        query = query.where(search_filter)
        logger.info(f"添加搜索条件: {q}")
    
    # 获取总数
    count_query = select(func.count(News.id)).where(News.deleted_at.is_(None))
    if q:
        count_query = count_query.where(search_filter)
    
    result = await db.execute(count_query)
    total = result.scalar()
    logger.info(f"数据库总记录数: {total}")
    
    # 分页查询
    offset = (page - 1) * limit
    query = query.options(selectinload(News.creator)).order_by(News.created_at.desc()).offset(offset).limit(limit)
    logger.info(f"分页参数: offset={offset}, limit={limit}")
    
    result = await db.execute(query)
    news_list = result.scalars().all()
    logger.info(f"查询到的新闻数量: {len(news_list)}")
    
    # 添加创建者用户名
    news_with_creator = []
    for i, news in enumerate(news_list):
        logger.info(f"新闻 {i+1}: id={news.id}, title={news.title[:20]}..., creator_id={news.creator_id}")
        logger.info(f"  creator对象: {news.creator}")
        if news.creator:
            logger.info(f"  creator.username: {news.creator.username}")
        else:
            logger.info(f"  creator为None")
            
        # 处理图片URL
        full_image_url = get_full_image_url(news.image_url)
        logger.info(f"  原始图片URL: {news.image_url}, 完整图片URL: {full_image_url}")
        
        news_dict = {
            "id": news.id,
            "title": news.title,
            "description": news.description,
            "image_url": full_image_url,
            "creator_id": news.creator_id,
            "created_at": news.created_at,
            "updated_at": news.updated_at,
            "creator_username": news.creator.username if news.creator else None
        }
        news_with_creator.append(NewsSchema(**news_dict))
    
    total_pages = ceil(total / limit) if total > 0 else 0
    logger.info(f"返回结果: items={len(news_with_creator)}, total={total}, total_pages={total_pages}")
    logger.info(f"=== 新闻列表查询结束 ===")
    
    return NewsListResponse(
        items=news_with_creator,
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages
    )


@router.get("/{id}", response_model=NewsSchema)
async def get_news(
    *,
    db: AsyncSession = Depends(get_db),
    id: int
) -> Any:
    """获取单个新闻详情（公开接口）"""
    result = await db.execute(
        select(News).options(selectinload(News.creator)).where(
            and_(News.id == id, News.deleted_at.is_(None))
        )
    )
    news = result.scalar_one_or_none()
    
    if not news:
        raise HTTPException(status_code=404, detail="新闻未找到")
    
    # 处理图片URL
    full_image_url = get_full_image_url(news.image_url)
    logger.info(f"获取新闻详情 - 原始图片URL: {news.image_url}, 完整图片URL: {full_image_url}")
    
    return NewsSchema(
        id=news.id,
        title=news.title,
        description=news.description,
        image_url=full_image_url,
        creator_id=news.creator_id,
        created_at=news.created_at,
        updated_at=news.updated_at,
        creator_username=news.creator.username if news.creator else None
    )


@router.post("/", response_model=NewsSchema, status_code=status.HTTP_201_CREATED)
async def create_news(
    *,
    db: AsyncSession = Depends(get_db),
    news_in: NewsCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """创建新闻（需要认证）"""
    db_news = News(
        title=news_in.title,
        description=news_in.description,
        image_url=news_in.image_url,
        creator_id=current_user.id
    )
    db.add(db_news)
    await db.commit()
    await db.refresh(db_news)
    
    # 加载创建者信息
    await db.refresh(db_news, ["creator"])
    
    # 处理图片URL
    full_image_url = get_full_image_url(db_news.image_url)
    logger.info(f"创建新闻 - 原始图片URL: {db_news.image_url}, 完整图片URL: {full_image_url}")
    
    return NewsSchema(
        id=db_news.id,
        title=db_news.title,
        description=db_news.description,
        image_url=full_image_url,
        creator_id=db_news.creator_id,
        created_at=db_news.created_at,
        updated_at=db_news.updated_at,
        creator_username=db_news.creator.username
    )


@router.put("/{id}", response_model=NewsSchema)
async def update_news(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
    news_in: NewsUpdate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """更新新闻（需要认证和所有权）"""
    result = await db.execute(
        select(News).where(and_(News.id == id, News.deleted_at.is_(None)))
    )
    news = result.scalar_one_or_none()
    
    if not news:
        raise HTTPException(status_code=404, detail="新闻未找到")
    
    # 检查权限：只有创建者或管理员可以编辑
    if news.creator_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限操作此新闻"
        )
    
    # 更新字段
    update_data = news_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(news, field, value)
    
    await db.commit()
    await db.refresh(news)
    
    # 加载创建者信息
    await db.refresh(news, ["creator"])
    
    # 处理图片URL
    full_image_url = get_full_image_url(news.image_url)
    logger.info(f"更新新闻 - 原始图片URL: {news.image_url}, 完整图片URL: {full_image_url}")
    
    return NewsSchema(
        id=news.id,
        title=news.title,
        description=news.description,
        image_url=full_image_url,
        creator_id=news.creator_id,
        created_at=news.created_at,
        updated_at=news.updated_at,
        creator_username=news.creator.username
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_news(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> None:
    """删除新闻（软删除，需要认证和所有权）"""
    result = await db.execute(
        select(News).where(and_(News.id == id, News.deleted_at.is_(None)))
    )
    news = result.scalar_one_or_none()
    
    if not news:
        raise HTTPException(status_code=404, detail="新闻未找到")
    
    # 检查权限：只有创建者或管理员可以删除
    if news.creator_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限操作此新闻"
        )
    
    # 软删除
    news.deleted_at = func.now()
    await db.commit()
    
    return None


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_image(
    *,
    image: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """上传图片（需要认证）"""
    logger.info(f"=== 图片上传开始 ===")
    logger.info(f"用户: {current_user.username}, 文件名: {image.filename}, 文件类型: {image.content_type}")
    
    # 检查文件类型
    if not image.content_type or not image.content_type.startswith('image/'):
        logger.error(f"不支持的文件类型: {image.content_type}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只支持图片文件"
        )
    
    # 检查文件大小（限制为5MB）
    max_size = 5 * 1024 * 1024  # 5MB
    content = await image.read()
    if len(content) > max_size:
        logger.error(f"文件过大: {len(content)} bytes")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="文件大小不能超过5MB"
        )
    
    # 生成唯一文件名
    file_extension = os.path.splitext(image.filename)[1] if image.filename else '.jpg'
    unique_filename = f"{uuid.uuid4().hex}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_extension}"
    
    # 确保上传目录存在
    upload_dir = settings.UPLOAD_DIR
    if not os.path.isabs(upload_dir):
        # 直接使用backend目录下的uploads
        # __file__ 是 backend/app/api/v1/endpoints/news.py，向上五级到backend目录
        backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        upload_dir = os.path.join(backend_dir, upload_dir)
    
    logger.info(f"计算的上传目录路径: {upload_dir}")
    
    os.makedirs(upload_dir, exist_ok=True)
    
    # 保存文件
    file_path = os.path.join(upload_dir, unique_filename)
    logger.info(f"保存文件到: {file_path}")
    
    try:
        with open(file_path, "wb") as f:
            f.write(content)
        
        # 返回相对路径，用于存储到数据库
        relative_path = unique_filename
        logger.info(f"文件上传成功: {relative_path}")
        logger.info(f"=== 图片上传结束 ===")
        
        return {
            "message": "图片上传成功",
            "filename": relative_path,
            "url": get_full_image_url(relative_path)
        }
    
    except Exception as e:
        logger.error(f"文件保存失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="文件保存失败"
        )
