from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt
from sqlmodel import Session
from ..database import get_session
from ..auth import oauth2_scheme
from ..config import settings
from ..models import UserPublic, TokenData
from ..crud import get_user_by_username

router = APIRouter(prefix="/users", tags=["users"])

async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: None | str = payload.get("sub")

        if username is None:
            print("Username not found.")
            raise credentials_exception

        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception

    user = get_user_by_username(session, username=token_data.username)

    if user is None:
        print("User not found.")
        raise credentials_exception

    return user

@router.get("/me", response_model=UserPublic)
def read_users_me(current_user: UserPublic = Depends(get_current_user)):
    return current_user
