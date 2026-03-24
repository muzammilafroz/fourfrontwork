from typing import Optional
from sqlmodel import Field, SQLModel

class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    email: str = Field(unique=True)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

class UserCreate(UserBase):
    password: str

class UserPublic(UserBase):
    id: int

class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    username: str = ""
