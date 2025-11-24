from pymongo import MongoClient
from app.config.settings import get_settings
from app.models.user import User, UserInDB
from app.models.token import Token, TokenInDB
from bson import ObjectId
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class MongoDBService:
    def __init__(self):
        self.settings = get_settings()
        self.client = None
        self.db = None
        self.connect()
    
    def connect(self):
        """Conecta ao MongoDB"""
        try:
            self.client = MongoClient(self.settings.mongodb_url)
            self.db = self.client[self.settings.database_name]
            logger.info("Conectado ao MongoDB com sucesso")
        except Exception as e:
            logger.error(f"Erro ao conectar ao MongoDB: {e}")
            raise
    
    def insert_user(self, user: User) -> str:
        """Insere usuário no MongoDB"""
        user_dict = user.dict()
        result = self.db.users.insert_one(user_dict)
        return str(result.inserted_id)
    
    def find_user_by_email(self, email: str) -> UserInDB:
        """Busca usuário por email"""
        user_data = self.db.users.find_one({"email": email})
        if user_data:
            user_data["id"] = str(user_data["_id"])
            return UserInDB(**user_data)
        return None
    
    def insert_token(self, token: Token) -> any:
        """Insere token no MongoDB"""
        token_dict = token.dict()
        return self.db.tokens.insert_one(token_dict)
    
    def find_token(self, token_str: str) -> TokenInDB:
        """Busca token por string"""
        token_data = self.db.tokens.find_one({"token": token_str})
        if token_data:
            token_data["id"] = str(token_data["_id"])
            return TokenInDB(**token_data)
        return None
    
    def find_token_by_email(self, email: str) -> TokenInDB:
        """Busca token por email"""
        token_data = self.db.tokens.find_one({"user_email": email, "used": False})
        if token_data:
            token_data["id"] = str(token_data["_id"])
            return TokenInDB(**token_data)
        return None
    
    def mark_token_used(self, token_str: str):
        """Marca token como usado"""
        self.db.tokens.update_one(
            {"token": token_str},
            {"$set": {"used": True, "used_at": datetime.now()}}
        )
    
    def mark_user_validated(self, email: str):
        """Marca usuário como validado"""
        self.db.users.update_one(
            {"email": email},
            {"$set": {"validated": True, "validation_date": datetime.now()}}
        )