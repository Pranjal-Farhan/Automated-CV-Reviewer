from fastapi import HTTPException, status
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from app.config.auth import (
    hash_password,
    verify_password,
    create_access_token,
    GOOGLE_CLIENT_ID,
)
from app.repository import user_repository
from app.models.user import UserCreate, UserLogin, UserResponse, TokenResponse


def _user_doc_to_response(doc: dict) -> UserResponse:
    return UserResponse(
        id=str(doc["_id"]),
        name=doc["name"],
        email=doc["email"],
        avatar=doc.get("avatar"),
        auth_provider=doc.get("auth_provider", "local"),
        created_at=doc["created_at"],
    )


def _build_token_response(doc: dict) -> TokenResponse:
    user_resp = _user_doc_to_response(doc)
    token = create_access_token(data={"sub": str(doc["_id"]), "email": doc["email"]})
    return TokenResponse(access_token=token, user=user_resp)


async def register(data: UserCreate) -> TokenResponse:
    existing = await user_repository.find_by_email(data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )
    user_doc = {
        "name": data.name,
        "email": data.email,
        "password_hash": hash_password(data.password),
        "avatar": None,
        "google_id": None,
        "auth_provider": "local",
    }
    created = await user_repository.create_user(user_doc)
    return _build_token_response(created)


async def login(data: UserLogin) -> TokenResponse:
    user = await user_repository.find_by_email(data.email)
    if not user or not user.get("password_hash"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    if not verify_password(data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    return _build_token_response(user)


async def google_auth(credential: str) -> TokenResponse:
    try:
        idinfo = id_token.verify_oauth2_token(
            credential, google_requests.Request(), GOOGLE_CLIENT_ID
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google token",
        )

    google_id = idinfo["sub"]
    email = idinfo["email"]
    name = idinfo.get("name", email.split("@")[0])
    avatar = idinfo.get("picture")

    # Check if user exists by google_id or email
    user = await user_repository.find_by_google_id(google_id)
    if not user:
        user = await user_repository.find_by_email(email)

    if user:
        # Update google info if needed
        await user_repository.update_user(
            str(user["_id"]),
            {"google_id": google_id, "avatar": avatar or user.get("avatar")},
        )
        user = await user_repository.find_by_id(str(user["_id"]))
    else:
        # Create new user
        user = await user_repository.create_user(
            {
                "name": name,
                "email": email,
                "password_hash": None,
                "avatar": avatar,
                "google_id": google_id,
                "auth_provider": "google",
            }
        )

    return _build_token_response(user)


async def get_current_user(user_id: str) -> UserResponse:
    user = await user_repository.find_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return _user_doc_to_response(user)