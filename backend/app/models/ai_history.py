from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.sql import func
import uuid
from app.db.database import Base


class AIHistory(Base):
    __tablename__ = "ai_history"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    device_id = Column(String, nullable=False, index=True)
    user_id = Column(String, nullable=False, index=True)
    prompt = Column(String, nullable=False)
    generated_plan = Column(JSON, nullable=True)
    result = Column(JSON, nullable=True)
    timestamp = Column(DateTime, server_default=func.now())