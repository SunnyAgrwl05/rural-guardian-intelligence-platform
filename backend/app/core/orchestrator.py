from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.agents.router import IntentRouter
from app.core.model_router import build_model, DemoModel
from app.models import ChatMessage, AuditLog, UserSession

class Orchestrator:
    def __init__(self, registry):
        self.registry = registry
        self.router = IntentRouter()
        self.model = build_model()
        self.demo_model = DemoModel()

    async def run(self, db: Session, user_id: int, session_id: int, module_name: str, message: str):
        if not self.registry.get(module_name):
            raise HTTPException(status_code=404, detail="Unknown module")
        session = db.query(UserSession).filter_by(id=session_id, user_id=user_id).first()
        if not session:
            raise HTTPException(status_code=403, detail="Session does not belong to the authenticated user")
        route = self.router.route(message)
        try:
            answer = await self.model.complete(route, message)
            provider_mode = "model"
        except Exception:
            answer = await self.demo_model.complete(route, message)
            provider_mode = "demo-fallback"
        db.add(ChatMessage(session_id=session_id, role="user", content=message, module=route.agent))
        db.add(ChatMessage(session_id=session_id, role="assistant", content=answer, module=route.agent))
        db.add(AuditLog(user_id=user_id, action="assistant.request", detail=f"agent={route.agent};domain={route.domain};risk={route.risk};mode={provider_mode}"))
        db.commit()
        sources = ["Rural Guardian safety policy"]
        if provider_mode == "demo-fallback":
            sources.append("Demo safety context")
        return {"answer":answer,"agent":route.agent,"domain":route.domain,"risk":route.risk,"reason":route.reason,"sources":sources,"mode":provider_mode}
