from datetime import datetime, timedelta, timezone
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, Response, Request
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.security import *
from app.core.config import settings
from app.models import User, UserSession

router = APIRouter(prefix="/api/auth", tags=["auth"])
class Login(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=200)

@router.get("/csrf")
def csrf(response: Response):
    t = new_csrf()
    response.set_cookie(CSRF_COOKIE, t, httponly=False, secure=False, samesite="strict", max_age=3600)
    return {"csrf": t}

def _login_user(u: User, response: Response, db: Session):
    j = uuid4().hex
    s = UserSession(user_id=u.id, token_id=j, expires_at=datetime.now(timezone.utc) + timedelta(minutes=30))
    db.add(s); db.commit()
    response.set_cookie(COOKIE, make_token(u.id, u.role, j), httponly=True, secure=False, samesite="strict", max_age=1800)
    return {"id": u.id, "email": u.email, "role": u.role, "session_id": s.id}

@router.post("/login")
def login(body: Login, response: Response, db: Session = Depends(get_db)):
    u = db.query(User).filter_by(email=body.email.lower()).first()
    if not u or not u.active or not verify_password(body.password, u.password_hash):
        raise HTTPException(401, "Invalid credentials")
    return _login_user(u, response, db)

@router.post("/demo-login")
def demo_login(response: Response, db: Session = Depends(get_db)):
    if not settings.dev_seed or settings.env != "development":
        raise HTTPException(404, "Demo login disabled")
    u = db.query(User).filter_by(email="admin@example.com").first()
    if not u:
        raise HTTPException(503, "Demo user is not seeded")
    return _login_user(u, response, db)

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(COOKIE)
    return {"ok": True}

def current_user(request: Request, db: Session = Depends(get_db)):
    t = request.cookies.get(COOKIE)
    if not t: raise HTTPException(401, "Not authenticated")
    p = decode_token(t)
    s = db.query(UserSession).filter_by(token_id=p["jti"], user_id=int(p["sub"])).first()
    if not s or s.expires_at < datetime.now(timezone.utc): raise HTTPException(401, "Session expired")
    u = db.get(User, int(p["sub"]))
    if not u or not u.active: raise HTTPException(401, "Inactive user")
    return u

@router.get("/me", name="auth_me")
def auth_me(user=Depends(current_user)):
    return {"id": user.id, "email": user.email, "role": user.role}
