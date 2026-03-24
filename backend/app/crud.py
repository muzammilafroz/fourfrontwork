from sqlmodel import Session, select
from .models import User, UserCreate
from .auth import get_password_hash

def get_user_by_username(session: Session, username: str):
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()

def create_user(session: Session, user_in: UserCreate):
    hashed_pw = get_password_hash(user_in.password)
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_pw
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
