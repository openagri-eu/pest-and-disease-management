import subprocess
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api.api_v1.api import api_router
from core.config import settings
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
import os
from init.db_init import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Sleep necessary because the db might not be up before this call, which results in a crash (restart the backend container for it to work properly though)

    # auto migrate the db
    time.sleep(3)
    subprocess.run(["alembic", "revision", "--autogenerate"], check=True)
    subprocess.run(["alembic", "upgrade", "head"], check=True)
    time.sleep(1)
    init_db()

    yield

app = FastAPI(
    title="OpenAgri", openapi_url="/api/v1/openapi.json", lifespan=lifespan
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
