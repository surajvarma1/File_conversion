"""Application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.image_tools.routes import router as image_router
from app.api.v1.pdf_tools.routes import router as pdf_router
from app.api.v1.zip_tools.routes import router as zip_router
from app.core.config import get_settings
from app.core.logging import get_logger, setup_logging
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.request_size import RequestSizeLimitMiddleware
from app.middleware.request_logger import RequestLoggerMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.core.container import Container
from app.utils.cleanup import periodic_cleanup
from app.api.v1.downloads.routes import router as download_router

import asyncio

settings = get_settings()
setup_logging(settings)
logger = get_logger(__name__)

app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# 1. Define the origins that are allowed to make requests
origins = [
    "http://localhost:3000",  # Your Next.js local development server
    "http://localhost:8000",  # Swagger UI / Backend itself
    # "https://your-production-domain.com" # Add this later when you deploy
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Allows your frontend
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    RateLimitMiddleware,
    max_requests=settings.RATE_LIMIT_REQUESTS,
    period_seconds=settings.RATE_LIMIT_PERIOD,
)

# Enforce Content-Length upper bound early
app.add_middleware(RequestSizeLimitMiddleware)
app.add_middleware(RequestLoggerMiddleware)
app.add_middleware(SecurityHeadersMiddleware)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(str(exc))
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


@app.get("/")
async def health_check():
    return {"status": "ok", "message": "File Conversion API is running"}

app.include_router(image_router, prefix=f"{settings.API_V1_STR}")
app.include_router(pdf_router, prefix=f"{settings.API_V1_STR}")
app.include_router(zip_router, prefix=f"{settings.API_V1_STR}")
app.include_router(download_router, prefix=f"{settings.API_V1_STR}")

# Dependency Injection container
container = Container()


@app.on_event("startup")
async def app_startup():
    # Wire container if necessary and start background cleanup
    app.state.container = container
    settings = container.config()
    storage = container.local_storage()

    # Start cleanup task
    stop_event = asyncio.Event()
    app.state._cleanup_stop_event = stop_event
    app.state._cleanup_task = asyncio.create_task(
        periodic_cleanup(
            storage,
            settings.TEMP_FILE_TTL,
            settings.AUTO_CLEANUP_INTERVAL,
            stop_event,
        )
    )


@app.on_event("shutdown")
async def app_shutdown():
    # Stop cleanup task
    stop_event = getattr(app.state, "_cleanup_stop_event", None)
    task = getattr(app.state, "_cleanup_task", None)
    if stop_event and not stop_event.is_set():
        stop_event.set()
    if task:
        task.cancel()
