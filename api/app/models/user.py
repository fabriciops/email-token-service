from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    nome: str
    email: EmailStr
    telefone: str
    cpf: str
    created_at: datetime = datetime.now()
    validated: bool = False
    validation_date: Optional[datetime] = None

class UserInDB(User):
    id: str

class UserResponse(BaseModel):
    id: str
    nome: str
    email: EmailStr
    validated: bool
    created_at: datetime