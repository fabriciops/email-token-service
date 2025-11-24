import sys
import os
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    # RabbitMQ
    rabbitmq_url: str
    
    # SMTP
    smtp_server: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    from_email: str
    
    # Application
    api_base_url: str
    
    # Configuração do Pydantic v2
    model_config = ConfigDict(env_file="/app/.env")

def get_settings():
    return Settings()