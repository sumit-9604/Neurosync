import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.core.security import hash_password, verify_password, create_access_token

logger = logging.getLogger("auth")
router = APIRouter()

# In-memory store for MVP — replace with DB later
_users: dict = {}


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/register")
async def register(req: RegisterRequest):
    if req.email in _users:
        raise HTTPException(status_code=400, detail="Email already registered")
    _users[req.email] = hash_password(req.password)
    logger.info(f"User registered: {req.email}")
    return {"message": "Registered successfully"}


@router.post("/login")
async def login(req: LoginRequest):
    hashed = _users.get(req.email)
    if not hashed or not verify_password(req.password, hashed):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": req.email})
    logger.info(f"User logged in: {req.email}")
    return {"access_token": token, "token_type": "bearer"}