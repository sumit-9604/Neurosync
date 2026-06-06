from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.sql import func
import uuid
from app.db.database import Base


class Command(Base):
    __tablename__ = "commands"

    command_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    device_id = Column(String, nullable=False, index=True)
    action = Column(String, nullable=False)
    payload = Column(JSON, nullable=True)
    status = Column(String, default="pending")  # pending | sent | success | failed
    result = Column(JSON, nullable=True)
    timestamp = Column(DateTime, server_default=func.now())