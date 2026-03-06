import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from app.api.routes import router
from app.config.database import connect_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    print("✅ Connected to MongoDB")
    yield
    await close_db()
    print("🔌 Disconnected from MongoDB")


app = FastAPI(
    title="Automated CV Reviewer",
    description="Upload a CV/Resume PDF → Get AI-powered analysis",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "service": "Automated CV Reviewer",
        "version": "1.0.0",
        "docs": "/docs",
    }