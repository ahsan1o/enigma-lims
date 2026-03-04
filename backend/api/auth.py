from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from database import get_db
from models import User
from utils.auth import verify_password, create_access_token, hash_password
from api.schemas import LoginRequest, TokenResponse, UserResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if not user.is_active:
        raise HTTPException(status_code=401, detail="Account is disabled")

    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()

    token = create_access_token({"sub": user.username, "role": user.role})
    return TokenResponse(
        access_token=token,
        user={
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role,
            "email": user.email
        }
    )

@router.post("/logout")
def logout():
    return {"message": "Logged out successfully"}

@router.get("/me", response_model=UserResponse)
def get_me(db: Session = Depends(get_db), authorization: str = None):
    # This will be called with the auth dependency from main app
    pass
