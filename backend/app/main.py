"""
CancerCareSystem API - Production Main Entry Point
"""

import os
import time
import traceback
from collections import defaultdict
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routes.predict import router as predict_router
from app.routes.auto_predict_route import router as auto_predict_router
from app.routes.blood_predict import router as blood_predict_router
from app.routes.brain_predict import router as brain_predict_router
from app.routes.skin_predict import router as skin_predict_router
from app.routes.breast_predict import router as breast_predict_router
from app.routes.auth import router as auth_router
from app.routes.otp import router as otp_router
from app.routes.history import router as history_router
from app.routes.wellness import router as wellness_router
from app.routes.donations import router as donations_router
from app.routes.wig_marketplace import router as wig_marketplace_router
from app.routes.staging import router as staging_router
from app.routes.profile import router as profile_router
from app.routes.medicine_reminders import router as medicine_reminders_router

app = FastAPI(
    title="CancerCareSystem API",
    description="Unified backend API for Bone, Lung, Brain, Blood, Skin & Breast Cancer detection using ML",
    version="7.0"
)

# --- CORS: restrict origins in production, allow all in dev ---
ALLOWED_ORIGINS = os.environ.get(
    "CORS_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174,http://localhost:3000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


# --- Global error handler: never leak raw tracebacks to client ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"ERROR: Unhandled error on {request.method} {request.url.path}: {exc}")
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc) if os.environ.get("DEBUG") else "An unexpected error occurred",
        },
    )


# --- In-memory rate limiter ---
_rate_limit_store: dict[str, list[float]] = defaultdict(list)
RATE_LIMIT_GENERAL = int(os.environ.get("RATE_LIMIT_GENERAL", "60"))  # per minute
RATE_LIMIT_AUTH = int(os.environ.get("RATE_LIMIT_AUTH", "100"))         # per minute
MAX_UPLOAD_SIZE = int(os.environ.get("MAX_UPLOAD_MB", "50")) * 1024 * 1024  # bytes


def _is_rate_limited(client_ip: str, path: str) -> bool:
    """Check if a client IP is rate-limited."""
    now = time.time()
    key = f"{client_ip}:{path.split('/')[1] if '/' in path else 'general'}"
    
    # Clean old entries (older than 60 seconds)
    _rate_limit_store[key] = [t for t in _rate_limit_store[key] if now - t < 60]
    
    # Choose limit based on path
    limit = RATE_LIMIT_AUTH if "/auth/" in path or "/otp/" in path else RATE_LIMIT_GENERAL
    
    if len(_rate_limit_store[key]) >= limit:
        return True
    
    _rate_limit_store[key].append(now)
    return False


# --- Security + rate limiting + logging middleware ---
@app.middleware("http")
async def security_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client else "unknown"
    path = request.url.path
    
    # Skip rate limiting for health checks and docs
    if path not in ("/health", "/", "/docs", "/openapi.json"):
        if _is_rate_limited(client_ip, path):
            return JSONResponse(
                status_code=429,
                content={"error": "Too many requests. Please try again later."}
            )
    
    # Check upload size for POST requests
    content_length = request.headers.get("content-length")
    if request.method == "POST" and content_length:
        if int(content_length) > MAX_UPLOAD_SIZE:
            return JSONResponse(
                status_code=413,
                content={"error": f"File too large. Maximum size is {MAX_UPLOAD_SIZE // (1024*1024)}MB."}
            )
    
    # Process request
    start = time.time()
    response = await call_next(request)
    elapsed = round((time.time() - start) * 1000)
    
    # Add security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    
    # Request logging
    print(f"REQ: {request.method} {path} -> {response.status_code} ({elapsed}ms) [{client_ip}]")

    return response


# --- Route registration ---
app.include_router(predict_router)
app.include_router(auto_predict_router)
app.include_router(blood_predict_router)
app.include_router(brain_predict_router)
app.include_router(skin_predict_router)
app.include_router(breast_predict_router)
app.include_router(auth_router)
app.include_router(otp_router)
app.include_router(history_router)
app.include_router(wellness_router)
app.include_router(donations_router)
app.include_router(wig_marketplace_router)
app.include_router(staging_router)
app.include_router(profile_router)
app.include_router(medicine_reminders_router)


@app.get("/")
def root():
    return {"status": "Backend is running successfully", "version": "6.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": time.time()}


if __name__ == "__main__":
    import uvicorn
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))
    debug = os.environ.get("DEBUG", "false").lower() == "true"
    uvicorn.run("app.main:app", host=host, port=port, reload=debug)
