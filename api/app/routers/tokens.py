from fastapi import APIRouter, HTTPException
from app.schemas.token import TokenValidationResponse
from app.services.token_service import TokenService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
token_service = TokenService()

@router.get("/validate-token/{token}", response_model=TokenValidationResponse)
async def validate_token(token: str):
    """
    Valida token recebido por email
    """
    try:
        valid, message = token_service.validate_token(token)
        
        if valid:
            token_data = token_service.mongo_service.find_token(token)
            return TokenValidationResponse(
                valid=True,
                user_email=token_data.user_email,
                message=message,
                validated_at=token_data.used_at
            )
        else:
            return TokenValidationResponse(
                valid=False,
                user_email="",
                message=message
            )
            
    except Exception as e:
        logger.error(f"Erro ao validar token: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")