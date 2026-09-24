from datetime import datetime,timezone
from sqlalchemy import String,Text,DateTime,ForeignKey,Boolean
from sqlalchemy.orm import Mapped,mapped_column
from pgvector.sqlalchemy import Vector
from app.core.db import Base
def now(): return datetime.now(timezone.utc)
class User(Base):
    __tablename__="users"; id:Mapped[int]=mapped_column(primary_key=True); email:Mapped[str]=mapped_column(String(320),unique=True,index=True); password_hash:Mapped[str]=mapped_column(String(512)); role:Mapped[str]=mapped_column(String(30),default="user"); active:Mapped[bool]=mapped_column(Boolean,default=True)
class UserSession(Base):
    __tablename__="sessions"; id:Mapped[int]=mapped_column(primary_key=True); user_id:Mapped[int]=mapped_column(ForeignKey("users.id")); token_id:Mapped[str]=mapped_column(String(64),unique=True,index=True); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now); expires_at:Mapped[datetime]=mapped_column(DateTime(timezone=True))
class ChatMessage(Base):
    __tablename__="messages"; id:Mapped[int]=mapped_column(primary_key=True); session_id:Mapped[int]=mapped_column(ForeignKey("sessions.id"),index=True); role:Mapped[str]=mapped_column(String(20)); content:Mapped[str]=mapped_column(Text); module:Mapped[str|None]=mapped_column(String(100),nullable=True); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
class AuditLog(Base):
    __tablename__="audit_logs"; id:Mapped[int]=mapped_column(primary_key=True); user_id:Mapped[int|None]=mapped_column(ForeignKey("users.id"),nullable=True); action:Mapped[str]=mapped_column(String(120)); detail:Mapped[str]=mapped_column(Text,default=""); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
class MemoryEmbedding(Base):
    __tablename__="memory_embeddings"; id:Mapped[int]=mapped_column(primary_key=True); user_id:Mapped[int]=mapped_column(ForeignKey("users.id")); text:Mapped[str]=mapped_column(Text); embedding:Mapped[list]=mapped_column(Vector(1536))
