from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import require_csrf
from app.core.rate_limit import rate_limit
from app.api.auth import current_user

router = APIRouter(prefix="/api/chat", tags=["chat"])
orchestrator = None

class ChatIn(BaseModel):
    session_id: int = Field(gt=0)
    module: str = Field(min_length=1, max_length=100)
    message: str = Field(min_length=1, max_length=6000)

@router.post("")
async def chat(body: ChatIn, request: Request, db: Session = Depends(get_db), user = Depends(current_user)):
    rate_limit(request)
    require_csrf(request)
    if orchestrator is None:
        raise HTTPException(status_code=503, detail="Orchestrator unavailable")
    return await orchestrator.run(db, user.id, body.session_id, body.module, body.message)
