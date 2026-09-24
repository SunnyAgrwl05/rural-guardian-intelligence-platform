from pathlib import Path
from time import perf_counter
from uuid import uuid4
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.core.config import settings
from app.core.registry import ModuleRegistry
from app.core.orchestrator import Orchestrator
from app.core.db import SessionLocal
from app.core.init_db import init_db
from app.api import auth, chat, admin

registry = ModuleRegistry(str(Path(__file__).parent / "modules"))
registry.discover()
init_db()
chat.orchestrator = Orchestrator(registry)

app = FastAPI(title=settings.app_name, version=settings.app_version, docs_url="/docs", redoc_url="/redoc")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in settings.cors_origins.split(",") if x.strip()],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-CSRF-Token", "X-Request-ID"],
)

@app.middleware("http")
async def security_headers(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or uuid4().hex
    started = perf_counter()
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Cache-Control"] = "no-store" if request.url.path.startswith("/api/") else "public, max-age=300"
    response.headers["X-Response-Time-ms"] = str(round((perf_counter() - started) * 1000, 2))
    return response

app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(admin.router)

@app.get("/api/health")
def health():
    return {"status": "ok", "service": settings.app_name, "version": settings.app_version, "model_provider": settings.model_provider}

@app.get("/api/readiness")
def readiness():
    db_ok = redis_ok = False
    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        pass
    try:
        from app.core.rate_limit import redis
        redis.ping()
        redis_ok = True
    except Exception:
        pass
    ready = db_ok and redis_ok
    return {"status": "ready" if ready else "degraded", "database": db_ok, "redis": redis_ok, "model_provider": settings.model_provider}

@app.get("/api/metrics")
def metrics():
    # Lightweight application metrics endpoint; detailed telemetry can be exported to App Insights/OpenTelemetry later.
    return {"service": settings.app_name, "version": settings.app_version, "registered_modules": len(registry.modules), "model_provider": settings.model_provider}

@app.get("/api/modules")
def modules():
    return [{"name": m.name, "version": m.version, "description": m.description, "tools": m.tools, "risky": m.risky} for m in registry.modules.values()]
