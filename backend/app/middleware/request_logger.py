"""Request logging middleware."""

import time
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import get_logger

logger = get_logger(__name__)


class RequestLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        client = request.client.host if request.client else "unknown"
        method = request.method
        path = request.url.path
        response = None
        try:
            response = await call_next(request)
            return response
        finally:
            duration = (time.time() - start) * 1000
            status_code = getattr(response, "status_code", "-") if response is not None else "-"
            logger.info(
                {
                    "client": client,
                    "method": method,
                    "path": path,
                    "duration_ms": round(duration, 2),
                    "status_code": status_code,
                }
            )
