from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    token: str
    user_email: str
    user_cpf: str
    session_id: Optional[str] = None  # ← NOVO CAMPO
    created_at: datetime = datetime.now()
    expires_at: datetime
    used: bool = False
    used_at: Optional[datetime] = None

class TokenInDB(Token):
    id: str

class TokenValidationResponse(BaseModel):
    valid: bool
    user_email: str
    message: str
    validated_at: Optional[datetime] = None