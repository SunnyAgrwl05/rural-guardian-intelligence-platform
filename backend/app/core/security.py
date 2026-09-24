from datetime import datetime,timedelta,timezone
from secrets import token_urlsafe
from jose import jwt,JWTError
from argon2 import PasswordHasher
from fastapi import Request,HTTPException
from app.core.config import settings
ph=PasswordHasher(); COOKIE="rg_session"; CSRF_COOKIE="rg_csrf"
def hash_password(p): return ph.hash(p)
def verify_password(p,h):
    try: ph.verify(h,p); return True
    except Exception: return False
def make_token(uid,role,jti):
    exp=datetime.now(timezone.utc)+timedelta(minutes=30)
    return jwt.encode({"sub":str(uid),"role":role,"jti":jti,"exp":exp},settings.secret_key,algorithm="HS256")
def decode_token(t):
    try: return jwt.decode(t,settings.secret_key,algorithms=["HS256"])
    except JWTError: raise HTTPException(401,"Invalid or expired session")
def new_csrf(): return token_urlsafe(32)
def require_csrf(r:Request):
    if r.cookies.get(CSRF_COOKIE)!=r.headers.get("X-CSRF-Token"): raise HTTPException(403,"CSRF validation failed")
