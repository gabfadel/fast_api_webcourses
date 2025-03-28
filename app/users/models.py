from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel):
    __tablename__ = "user"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    password_hash: str
    phone: Optional[str] = None
