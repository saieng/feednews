from typing import Any, Optional
from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query, status
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

router = APIRouter()


@router.get("/", response_model=NewsListResponse)
async def read_news(
    db: AsyncSession = Depends(get_db),
    page: int = Query(default=1, ge=1, description="页码"),
    limit: int = Query(default=10, ge=1, le=100, description="每页数量"),
    q: Optional[str] = Query(default=None, description="搜索关键词")
) -> Any:
    """获取新闻列表（公开接口）"""
    # 构建查询条件
    query = select(News).where(News.deleted_at.is_(None))
    
    # 添加搜索条件
    if q:
        search_filter = or_(
            News.title.ilike(f"%{q}%"),
            News.description.ilike(f"%{q}%")
        )
        query = query.where(search_filter)
    
    # 获取总数
    count_query = select(func.count(News.id)).where(News.deleted_at.is_(None))
    if q:
        count_query = count_query.where(search_filter)
    
    result = await db.execute(count_query)
    total = result.scalar()
    
    # 分页查询
    offset = (page - 1) * limit
    query = query.options(selectinload(News.creator)).order_by(News.created_at.desc()).offset(offset).limit(limit)
    
    result = await db.execute(query)
    news_list = result.scalars().all()
    
    # 添加创建者用户名
    news_with_creator = []
    for news in news_list:
        news_dict = {
            "id": news.id,
            "title": news.title,
            "description": news.description,
            "image_url": news.image_url,
            "creator_id": news.creator_id,
            "created_at": news.created_at,
            "updated_at": news.updated_at,
            "creator_username": news.creator.username if news.creator else None
        }
        news_with_creator.append(NewsSchema(**news_dict))
    
    total_pages = ceil(total / limit) if total > 0 else 0
    
    return NewsListResponse(
        items=news_with_creator,
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages
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
    
    return NewsSchema(
        id=db_news.id,
        title=db_news.title,
        description=db_news.description,
        image_url=db_news.image_url,
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
    
    return NewsSchema(
        id=news.id,
        title=news.title,
        description=news.description,
        image_url=news.image_url,
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
) -> Any:
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