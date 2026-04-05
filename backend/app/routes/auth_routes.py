from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from ..auth import create_access_token, verify_password
from ..crud import create_user, get_user_by_email
from ..database import get_session
from ..models import TokenPublic, UserCreate, UserPublic, UserStatus

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic)
def register(user_in: UserCreate, session: Session = Depends(get_session)):
    user = get_user_by_email(session, user_in.email)

    if user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    return create_user(session, user_in)


@router.post("/login", response_model=TokenPublic)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    email = form_data.username
    user = get_user_by_email(session, email)

    if (not user) or (not verify_password(form_data.password, user.hashed_password)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password.")

    if user.status == UserStatus.INACTIVE:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Your account is inactive. Please contact admin.")

    access_token = create_access_token(
        data={
            "sub": user.email,
            "role": user.role,
        }
    )

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Bad request."
        )

    return {"access_token": access_token, "token_type": "bearer", "user": user}
