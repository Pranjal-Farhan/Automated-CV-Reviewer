from fastapi import HTTPException, status

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
    """
    Handle Google OAuth.
    The frontend sends an access_token from Google's OAuth popup.
    We try two methods:
      1. Use it as an access_token to fetch user info from Google API
      2. Fall back to verifying it as an id_token
    """
    import requests as req

    user_info = None

    # ── Method 1: Treat credential as access_token ──
    try:
        google_resp = req.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {credential}"},
            timeout=10,
        )
        if google_resp.status_code == 200:
            data = google_resp.json()
            if data.get("sub"):
                user_info = data
    except Exception:
        pass

    # ── Method 2: Treat credential as id_token ──
    if not user_info:
        try:
            from google.oauth2 import id_token
            from google.auth.transport import requests as google_requests

            user_info = id_token.verify_oauth2_token(
                credential, google_requests.Request(), GOOGLE_CLIENT_ID
            )
        except Exception:
            pass

    # ── If both methods failed ──
    if not user_info or not user_info.get("sub"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google token",
        )

    google_id = user_info["sub"]
    email = user_info.get("email", "")
    name = user_info.get("name", email.split("@")[0])
    avatar = user_info.get("picture")

    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google account has no email",
        )

    # Check if user exists by google_id or email
    user = await user_repository.find_by_google_id(google_id)
    if not user:
        user = await user_repository.find_by_email(email)

    if user:
        # Update google info
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