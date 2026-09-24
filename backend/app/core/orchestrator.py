from app.agents.router import IntentRouter
from app.core.model_router import build_model
from app.models import ChatMessage,AuditLog
class Orchestrator:
    def __init__(self,registry): self.registry=registry; self.router=IntentRouter(); self.model=build_model()
    async def run(self,db,user_id,session_id,module_name,message):
        if not self.registry.get(module_name): raise ValueError("Unknown module")
        route=self.router.route(message); answer=await self.model.complete(route,message)
        db.add(ChatMessage(session_id=session_id,role="user",content=message,module=route.agent)); db.add(ChatMessage(session_id=session_id,role="assistant",content=answer,module=route.agent)); db.add(AuditLog(user_id=user_id,action="assistant.request",detail=f"agent={route.agent};domain={route.domain};risk={route.risk}")); db.commit()
        return {"answer":answer,"agent":route.agent,"domain":route.domain,"risk":route.risk,"reason":route.reason,"sources":["Rural Guardian safety policy","Demo knowledge context"]}
