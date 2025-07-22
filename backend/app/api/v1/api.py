from fastapi import APIRouter

from app.api.v1.endpoints import auth, news, admin

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(news.router, prefix="/news", tags=["news"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])