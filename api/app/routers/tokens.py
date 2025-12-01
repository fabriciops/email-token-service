from fastapi import APIRouter, HTTPException, Request, Header
from app.schemas.token import TokenValidationResponse
from app.services.token_service import TokenService
from app.config.settings import get_settings
import logging
import httpx
import asyncio
from datetime import datetime
from app.utils.security import verify_api_hash
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

logger = logging.getLogger(__name__)

router = APIRouter()
token_service = TokenService()
settings = get_settings()

templates = Jinja2Templates(directory="app/templates")

@router.get("/validate-token/{token}", response_class=HTMLResponse)
async def validate_token(
    token: str, 
    request: Request,
    x_api_hash: str = Header(...),
    ):
    """
    Valida token recebido por email e retorna página HTML
    """
    try:
        logger.info(f"Validando token: {token}")
        
        if not verify_api_hash(x_api_hash):
            raise HTTPException(status_code=401, detail="API Hash inválido")
        
        valid, message = token_service.validate_token(token)
        logger.info(f"Resultado validação: {valid} - {message}")
        
        if valid:
            token_data = token_service.mongo_service.find_token(token)
            logger.info(f"Token data encontrado: {token_data}")
            logger.info(f"Email do token: {token_data.user_email if token_data else 'N/A'}")
            
            if not token_data:
                logger.error(f"Token data não encontrado para token: {token}")
                return templates.TemplateResponse(
                    "validation_error.html",
                    {
                        "request": request,
                        "message": "Token inválido ou não encontrado"
                    }
                )
            
            # Notificar Typebot em background
            asyncio.create_task(notify_typebot_validation(token_data))
            
            return templates.TemplateResponse(
                "validation_success.html",
                {
                    "request": request,
                    "user_email": token_data.user_email,
                    "validated_at": token_data.used_at if token_data.used_at else datetime.now(),
                    "message": "Token validado com sucesso!"
                }
            )
        else:
            logger.warning(f"Validação falhou: {message}")
            return templates.TemplateResponse(
                "validation_error.html",
                {
                    "request": request,
                    "message": message
                }
            )
            
    except Exception as e:
        logger.error(f"Erro ao validar token: {e}")
        return templates.TemplateResponse(
            "validation_server_error.html",
            {
                "request": request,
                "error_message": "Erro interno do servidor"
            },
            status_code=500
        )
        
        
async def notify_typebot_validation(token_data):
    """
    Notifica o Typebot que o usuário foi validado
    """
    try:
        if not settings.typebot_webhook_url or not settings.typebot_webhook_enabled:
            logger.info("Webhook do Typebot não configurado")
            return
        
        # Acessar campos como atributos do objeto
        user_email = token_data.user_email
        session_id = token_data.session_id
        token_str = token_data.token
        
        if not user_email:
            logger.error("Email não encontrado no token_data para notificar Typebot")
            return
        
        payload = {
            "event": "email_validated",
            "email": user_email,
            "sessionId": session_id,
            "validated": True,
            "validationTimestamp": datetime.now().isoformat(),
            "token": token_str
        }
        
        logger.info(f"Notificando Typebot para: {user_email}")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                settings.typebot_webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code in [200, 201, 204]:
                logger.info(f"Typebot notificado com sucesso: {user_email}")
            else:
                logger.warning(f"Typebot retornou status {response.status_code}: {response.text}")
                
    except Exception as e:
        logger.error(f"Erro ao notificar Typebot: {e}")