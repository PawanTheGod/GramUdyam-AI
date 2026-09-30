"""
GramUdyam AI – FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.database import engine
from app.models import Base
from app.seed import seed_database
from app.routers import auth, profiles, local_data, businesses, feasibility, financial, schemes, dashboard, reports, demo

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-Powered Local Business Discovery, Feasibility & Financial Advisory for Rural India",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(profiles.router)
app.include_router(local_data.router)
app.include_router(businesses.router)
app.include_router(feasibility.router)
app.include_router(financial.router)
app.include_router(schemes.router)
app.include_router(dashboard.router)
app.include_router(reports.router)
app.include_router(demo.router)


@app.on_event("startup")
def startup_event():
    """Create tables and seed on startup."""
    Base.metadata.create_all(bind=engine)
    seed_database()


@app.get("/", tags=["Health"])
def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "tagline": "AI-Powered Local Business Discovery, Feasibility & Financial Advisory",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "database": "connected"}
