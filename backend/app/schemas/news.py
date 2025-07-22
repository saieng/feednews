from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime


class NewsBase(BaseModel):
    title: str
    description: str
    image_url: Optional[str] = None


class NewsCreate(NewsBase):
    pass


class NewsUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None


class NewsInDBBase(NewsBase):
    id: int
    creator_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class News(NewsInDBBase):
    creator_username: Optional[str] = None


class NewsInDB(NewsInDBBase):
    deleted_at: Optional[datetime] = None


class NewsListResponse(BaseModel):
    items: list[News]
    total: int
    page: int
    limit: int
    total_pages: int