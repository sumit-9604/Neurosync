from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
import uuid
from app.db.database import Base


class Session(Base):
    __tablename__ = "sessions"

    session_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    device_id = Column(String, nullable=True)
    login_time = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime, nullable=True)