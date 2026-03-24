from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from ..database import get_session
from ..models import UserPublic, UserCreate, Token
from ..crud import get_user_by_username, create_user
from ..auth import verify_password, create_access_token
from datetime import timedelta
from ..config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserPublic)
def signup(user_in: UserCreate, session: Session = Depends(get_session)):
    user = get_user_by_username(session, user_in.username)
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(session, user_in)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = get_user_by_username(session, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
