from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt
from sqlmodel import Session

from ..auth import oauth2_scheme
from ..config import settings
from ..crud import get_user_by_email
from ..database import get_session
from ..models import Message, User, UserPublic

router = APIRouter(prefix="/user", tags=["user"])


async def get_current_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: None | str = payload.get("sub")

        if email is None:
            print("Email not found.")
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = get_user_by_email(session, email=email)

    if user is None:
        print("User not found.")
        raise credentials_exception

    return user


@router.get("/logout", response_model=Message)
def logout(_: UserPublic = Depends(get_current_user)):
    return {"detail": "Successfully logged out."}


@router.get("/me", response_model=UserPublic)
def read_users_me(current_user: UserPublic = Depends(get_current_user)):
    return current_user
