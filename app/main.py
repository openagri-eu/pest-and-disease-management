from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api.api_v1.api import api_router
from core.config import settings
from init.db_init import init_db

@asynccontextmanager
async def lifespan(fa: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="Pest and Disease Management", openapi_url="/api/v1/openapi.json", lifespan=lifespan
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix="/api/v1")
