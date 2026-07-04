"""Rate limiting middleware."""

import time

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import get_settings
from app.core.logging import get_logger

settings = get_settings()
logger = get_logger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiting."""

    def __init__(self, app, max_requests: int, period_seconds: int):
        super().__init__(app)
        self.max_requests = max_requests
        self.period_seconds = period_seconds
        self.clients: dict[str, list[float]] = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        if not self.max_requests or not self.period_seconds:
            return await call_next(request)

        current_time = time.time()
        request_times = self.clients.get(client_ip, [])
        request_times = [t for t in request_times if current_time - t < self.period_seconds]
        request_times.append(current_time)
        self.clients[client_ip] = request_times

        if len(request_times) > self.max_requests:
            logger.warning(f"Rate limit exceeded for {client_ip}")
            return JSONResponse(
                {"detail": "Rate limit exceeded. Try again later."},
                status_code=429,
            )

        return await call_next(request)
