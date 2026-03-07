from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class GoogleAuthRequest(BaseModel):
    credential: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    avatar: Optional[str] = None
    auth_provider: str = "local"
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class UserInDB(BaseModel):
    name: str
    email: str
    password_hash: Optional[str] = None
    avatar: Optional[str] = None
    google_id: Optional[str] = None
    auth_provider: str = "local"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)