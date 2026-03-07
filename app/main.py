import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from app.api.routes import router as cv_router
from app.api.auth_routes import router as auth_router
from app.config.database import connect_db, close_db
from app.repository.cv_repository import CVRepository
from app.repository import user_repository


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ──
    await connect_db()
    print("✅ Connected to MongoDB")

    # Create indexes for users and cv_jobs collections
    await user_repository.create_indexes()
    await CVRepository.create_indexes()
    print("✅ Database indexes created")

    yield

    # ── Shutdown ──
    await close_db()
    print("🔌 Disconnected from MongoDB")


app = FastAPI(
    title="Automated CV Reviewer",
    description="Upload a CV/Resume PDF → Get AI-powered analysis",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ──────────────────────────────────────────────────
# Allow the React frontend (Vite dev server + Docker production)
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000,http://localhost").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ────────────────────────────────────────────────
app.include_router(auth_router, prefix="/api/v1")
app.include_router(cv_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "service": "Automated CV Reviewer",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    return {"status": "ok"}