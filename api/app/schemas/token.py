from pydantic import BaseModel
from datetime import datetime

class TokenValidationRequest(BaseModel):
    token: str

class TokenValidationResponse(BaseModel):
    valid: bool
    user_email: str
    message: str
    validated_at: datetime = None