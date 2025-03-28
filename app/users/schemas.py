from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    password: str
    phone: Optional[str] = None

class UserOut(BaseModel):
    id: int
    name: str
    phone: Optional[str] = None

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
