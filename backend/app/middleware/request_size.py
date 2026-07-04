"""Middleware to enforce request size limits based on Content-Length."""

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import get_settings
from app.core.logging import get_logger

settings = get_settings()
logger = get_logger(__name__)


class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    """Reject requests with Content-Length exceeding max upload size."""

    async def dispatch(self, request: Request, call_next):
        # Only check when header present
        content_length = request.headers.get("content-length")
        if content_length:
            try:
                length = int(content_length)
                if length > settings.MAX_UPLOAD_SIZE:
                    logger.warning(f"Request rejected: content-length {length} exceeds limit")
                    return JSONResponse({"detail": "Request body too large"}, status_code=413)
            except ValueError:
                # Ignore malformed header and continue
                pass
        return await call_next(request)
