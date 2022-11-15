from fastapi import APIRouter

from app.api.api_v1.endpoints import login, users, institutions

api_router = APIRouter()
api_router.include_router(login.router, tags=['Authentication'])
api_router.include_router(users.router, prefix='/users', tags=['Users'])
api_router.include_router(institutions.router, tags=['Institutions'])