from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.core.security import decode_access_token
from app.core.dependencies import get_current_user

async def get_current_user(
    authorization: str = Header(...),
    db: Session = Depends(get_db)
) -> User:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")

    token = authorization.split(" ", 1)[1]
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(User).filter(User.user_id == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user