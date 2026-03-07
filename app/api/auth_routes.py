from fastapi import APIRouter, Depends

from app.models.user import (
    UserCreate,
    UserLogin,
    GoogleAuthRequest,
    UserResponse,
    TokenResponse,
)
from app.service import auth_service
from app.config.auth import get_current_user_id

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse)
async def register(data: UserCreate):
    return await auth_service.register(data)


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin):
    return await auth_service.login(data)


@router.post("/google", response_model=TokenResponse)
async def google_auth(data: GoogleAuthRequest):
    return await auth_service.google_auth(data.credential)


@router.get("/me", response_model=UserResponse)
async def get_me(user_id: str = Depends(get_current_user_id)):
    return await auth_service.get_current_user(user_id)