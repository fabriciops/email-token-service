from fastapi import APIRouter, HTTPException, Header
from app.schemas.user import UserCreateRequest, UserCreateResponse
from app.services.mongo_service import MongoDBService
from app.services.token_service import TokenService
from app.services.email_service import EmailService
from app.utils.security import verify_api_hash
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
mongo_service = MongoDBService()
token_service = TokenService()
email_service = EmailService()

@router.post("/receive-user-data", response_model=UserCreateResponse)
async def receive_user_data(user_data: UserCreateRequest, x_api_hash: str = Header(...)):
    """
    Recebe dados do usuário do Typebot e inicia processo de validação
    """
    try:
        # Validar hash da API - SIMPLES E DIRETO
        if not verify_api_hash(x_api_hash):
            raise HTTPException(status_code=401, detail="API Hash inválido")
        
        # Verificar se usuário já existe
        existing_user = mongo_service.find_user_by_email(user_data.email)
        if existing_user:
            if existing_user.validated:
                return UserCreateResponse(
                    success=True,
                    message="Usuário já validado anteriormente",
                    user_id=existing_user.id
                )
            else:
                # Reenviar token se não validado
                token = token_service.get_token_by_email(user_data.email)
                if token:
                    await email_service.send_validation_email(token, user_data.nome)
                    return UserCreateResponse(
                        success=True,
                        message="Token reenviado para validação",
                        user_id=existing_user.id
                    )
        
        # Criar novo usuário
        from app.models.user import User
        user = User(**user_data.dict())
        user_id = mongo_service.insert_user(user)
        
        # Gerar token
        token = token_service.create_token(user_data.email, user_data.cpf)
        
        # Enviar email (assíncrono)
        await email_service.send_validation_email(token, user_data.nome)
        
        return UserCreateResponse(
            success=True,
            message="Token de validação enviado por email",
            user_id=user_id
        )
        
    except Exception as e:
        logger.error(f"Erro ao processar dados do usuário: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")
