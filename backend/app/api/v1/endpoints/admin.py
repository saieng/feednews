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
from app.schemas.user import User as UserSchema

router = APIRouter()


@router.get("/news", response_model=NewsListResponse)
async def admin_read_news(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_admin_user),
    page: int = Query(default=1, ge=1, description="页码"),
    limit: int = Query(default=10, ge=1, le=100, description="每页数量"),
    q: Optional[str] = Query(default=None, description="搜索关键词"),
    include_deleted: bool = Query(default=False, description="是否包含已删除的新闻")
) -> Any:
    """管理员获取新闻列表（包含已删除的新闻）"""
    # 构建查询条件
    query = select(News)
    count_query = select(func.count(News.id))
    
    # 是否包含已删除的新闻
    if not include_deleted:
        query = query.where(News.deleted_at.is_(None))
        count_query = count_query.where(News.deleted_at.is_(None))
    
    # 添加搜索条件
    if q:
        search_filter = or_(
            News.title.ilike(f"%{q}%"),
            News.description.ilike(f"%{q}%")
        )
        query = query.where(search_filter)
        count_query = count_query.where(search_filter)
    
    # 获取总数
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


@router.delete("/news/{id}/force", status_code=status.HTTP_204_NO_CONTENT)
async def admin_force_delete_news(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
    current_user: User = Depends(deps.get_current_admin_user)
) -> None:
    """管理员强制删除新闻（物理删除）"""
    result = await db.execute(select(News).where(News.id == id))
    news = result.scalar_one_or_none()
    
    if not news:
        raise HTTPException(status_code=404, detail="新闻未找到")
    
    await db.delete(news)
    await db.commit()


@router.post("/news/{id}/restore", response_model=NewsSchema)
async def admin_restore_news(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
    current_user: User = Depends(deps.get_current_admin_user)
) -> Any:
    """管理员恢复已删除的新闻"""
    result = await db.execute(
        select(News).where(and_(News.id == id, News.deleted_at.is_not(None)))
    )
    news = result.scalar_one_or_none()
    
    if not news:
        raise HTTPException(status_code=404, detail="已删除的新闻未找到")
    
    # 恢复新闻
    news.deleted_at = None
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


@router.get("/users", response_model=list[UserSchema])
async def admin_read_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_admin_user),
    page: int = Query(default=1, ge=1, description="页码"),
    limit: int = Query(default=10, ge=1, le=100, description="每页数量")
) -> Any:
    """管理员获取用户列表"""
    offset = (page - 1) * limit
    result = await db.execute(
        select(User).order_by(User.created_at.desc()).offset(offset).limit(limit)
    )
    users = result.scalars().all()
    return users