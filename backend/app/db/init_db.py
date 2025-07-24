from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.security import get_password_hash
from app.models.user import User
from app.models.news import News
from app.db.base import Base
from app.db.session import engine


async def init_db() -> None:
    """初始化数据库"""
    # 创建所有表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # 预先计算密码哈希（在异步上下文外）
    admin_password_hash = get_password_hash("admin123")
    
    # 创建默认管理员用户
    async with AsyncSession(engine) as session:
        # 检查是否已存在管理员用户
        result = await session.execute(
            select(User).where(User.username == "admin")
        )
        admin_user = result.scalar_one_or_none()
        
        if not admin_user:
            admin_user = User(
                username="admin",
                email="admin@feednews.com",
                hashed_password=admin_password_hash,
                is_admin=True
            )
            session.add(admin_user)
            await session.commit()
            await session.refresh(admin_user)
            print("默认管理员用户已创建: admin / admin123")
        else:
            print("管理员用户已存在")
        
        # 创建一些示例新闻
        result = await session.execute(select(News))
        existing_news = result.scalars().first()
        
        if not existing_news:
            sample_news = [
                News(
                    title="欢迎来到 FeedNews",
                    description="这是一个现代化的新闻展示平台，采用 Vue3 + FastAPI 构建。我们致力于为用户提供最佳的阅读体验。",
                    image_url="https://via.placeholder.com/400x225/4F46E5/FFFFFF?text=Welcome+to+FeedNews",
                    creator_id=admin_user.id
                ),
                News(
                    title="技术栈介绍",
                    description="前端使用 Vue3 + TailwindCSS，后端采用 FastAPI + PostgreSQL，全部通过 Docker 容器化部署。",
                    image_url="https://via.placeholder.com/400x225/059669/FFFFFF?text=Tech+Stack",
                    creator_id=admin_user.id
                ),
                News(
                    title="响应式设计",
                    description="完美适配 PC、平板、手机等多设备场景，提供一致的用户体验。",
                    image_url="https://via.placeholder.com/400x225/DC2626/FFFFFF?text=Responsive+Design",
                    creator_id=admin_user.id
                ),
                News(
                    title="用户系统",
                    description="完整的注册登录体系，支持用户权限管理和新闻内容管理。",
                    image_url="https://via.placeholder.com/400x225/7C3AED/FFFFFF?text=User+System",
                    creator_id=admin_user.id
                ),
                News(
                    title="现代化动效",
                    description="复刻 feedmusic.com 的精致动效和交互体验，提供丝滑的滚动效果。",
                    image_url="https://via.placeholder.com/400x225/EA580C/FFFFFF?text=Modern+Effects",
                    creator_id=admin_user.id
                ),
                News(
                    title="容器化部署",
                    description="使用 Docker Compose 实现一键部署，支持开发和生产环境。",
                    image_url="https://via.placeholder.com/400x225/0891B2/FFFFFF?text=Docker+Deploy",
                    creator_id=admin_user.id
                )
            ]
            
            for news in sample_news:
                session.add(news)
            
            await session.commit()
            print(f"已创建 {len(sample_news)} 条示例新闻")
        else:
            print("示例新闻已存在")