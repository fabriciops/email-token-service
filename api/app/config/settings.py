from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    # API
    app_name: str = "DefensorTokenValidator API"
    secret_key: str
    api_hash_key: str
    
    # MongoDB
    mongodb_url: str
    database_name: str = "defensortokenvalidator"
    
    # RabbitMQ
    rabbitmq_url: str
    
    # Token
    token_expiration_minutes: int = 15
    
    # Security
    algorithm: str = "HS256"
    
    # Typebot Webhook
    typebot_webhook_url: str = ""
    typebot_webhook_enabled: bool = False
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()