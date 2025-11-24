from pydantic import BaseModel, EmailStr

class UserCreateRequest(BaseModel):
    nome: str
    email: EmailStr
    telefone: str
    cpf: str

class UserCreateResponse(BaseModel):
    success: bool
    message: str
    user_id: str

class UserValidationResponse(BaseModel):
    validated: bool
    message: str