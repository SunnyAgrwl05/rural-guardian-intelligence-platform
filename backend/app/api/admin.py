from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.api.auth import current_user
from app.models import AuditLog
router=APIRouter(prefix="/api/admin",tags=["admin"])
@router.get("/audit")
def audit(db:Session=Depends(get_db),user=Depends(current_user)):
    if user.role!="admin": raise HTTPException(403,"Admin role required")
    return [{"id":x.id,"user_id":x.user_id,"action":x.action,"detail":x.detail,"created_at":x.created_at} for x in db.query(AuditLog).order_by(AuditLog.id.desc()).limit(100)]
