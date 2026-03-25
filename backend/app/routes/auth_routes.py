from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from ..auth import create_access_token, verify_password
from ..config import settings
from ..crud import create_user, get_user_by_email
from ..database import get_session
from ..models import Token, UserCreate, UserPublic

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserPublic)
def signup(user_in: UserCreate, session: Session = Depends(get_session)):
    user = get_user_by_email(session, user_in.email)

    if user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    return create_user(session, user_in)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    email = form_data.username
    user = get_user_by_email(session, email)

    if (not user) or (not verify_password(form_data.password, user.hashed_password)):
        raise HTTPException(status_code=400, detail="Incorrect username or password.")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Bad request."
        )

    return {"access_token": access_token, "token_type": "bearer"}
