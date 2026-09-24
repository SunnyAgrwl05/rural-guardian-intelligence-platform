from redis import Redis
from fastapi import Request, HTTPException
from app.core.config import settings

redis = Redis.from_url(settings.redis_url, decode_responses=True, socket_connect_timeout=2, socket_timeout=2)

def rate_limit(r: Request):
    ip = r.client.host if r.client else "unknown"
    key = f"rg:rl:{ip}"
    try:
        n = redis.incr(key)
        if n == 1:
            redis.expire(key, 60)
        if n > settings.rate_limit_per_minute:
            raise HTTPException(429, "Rate limit exceeded")
    except HTTPException:
        raise
    except Exception:
        # Availability-first fallback: API remains usable if Redis is temporarily unavailable.
        return
