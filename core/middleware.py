from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from core.rate_limiter import RateLimiter
from core.security import decode_access_token

rate_limiter = RateLimiter(max_requests=10, window_seconds=60)

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth = request.headers.get("Authorization")

        if auth and auth.startswith("Bearer "):
            token = auth.split(" ")[1]
            payload = decode_access_token(token)
            key = f"user:{payload['sub']}"
        else: 
            key = f"ip:{request.client.host}"

        if not rate_limiter.is_allowed(key):
            return JSONResponse(
                status_code = 429,
                content = {"detail": "Too many requests"}
            )

        return await call_next(request)