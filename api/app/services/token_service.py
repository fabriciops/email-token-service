import secrets
import string
from datetime import datetime, timedelta
from app.config.settings import get_settings
from app.models.token import Token
from app.services.mongo_service import MongoDBService
import logging

logger = logging.getLogger(__name__)

class TokenService:
    def __init__(self):
        self.settings = get_settings()
        self.mongo_service = MongoDBService()
        self.token_length = 8
        logger.info("TokenService inicializado")
    
    def generate_token(self) -> str:
        """Gera um token alfanumérico seguro"""
        alphabet = string.ascii_uppercase + string.digits
        token = ''.join(secrets.choice(alphabet) for _ in range(self.token_length))
        logger.info(f"Token gerado: {token}")
        return token
    
    def create_token(self, user_email: str, user_cpf: str, session_id: str = None) -> Token:
        """Cria um novo token para validação"""
        try:
            logger.info(f"Criando token para: {user_email}")
            
            token_str = self.generate_token()
            expires_at = datetime.now() + timedelta(minutes=self.settings.token_expiration_minutes)
            
            token = Token(
                token=token_str,
                user_email=user_email,
                user_cpf=user_cpf,
                session_id=session_id,
                expires_at=expires_at
            )
            
            logger.info(f"Token criado: {token_str} para {user_email}")
            
            # Salvar no MongoDB
            result = self.mongo_service.insert_token(token)
            logger.info(f"Token salvo no MongoDB com ID: {result.inserted_id}")
            
            return token
            
        except Exception as e:
            logger.error(f"Erro ao criar token: {e}")
            raise
    
    def validate_token(self, token_str: str) -> tuple[bool, str]:
        """Valida um token"""
        try:
            token = self.mongo_service.find_token(token_str)
            
            if not token:
                return False, "Token não encontrado"
            
            if token.used:
                return False, "Token já utilizado"
            
            if datetime.now() > token.expires_at:
                return False, "Token expirado"
            
            # Marcar token como usado
            self.mongo_service.mark_token_used(token_str)
            
            # Marcar usuário como validado
            self.mongo_service.mark_user_validated(token.user_email)
            
            logger.info(f"Token validado com sucesso para {token.user_email}")
            return True, "Token validado com sucesso"
            
        except Exception as e:
            logger.error(f"Erro ao validar token: {e}")
            return False, f"Erro ao validar token: {str(e)}"
    
    def get_token_by_email(self, email: str):
        """Busca token por email"""
        return self.mongo_service.find_token_by_email(email)