import json
import aio_pika
from app.config.settings import get_settings
from app.models.token import Token
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.settings = get_settings()
        self.connection = None
        self.channel = None
    
    async def connect(self):
        """Conecta ao RabbitMQ"""
        if not self.connection:
            self.connection = await aio_pika.connect_robust(self.settings.rabbitmq_url)
            self.channel = await self.connection.channel()
            await self.channel.declare_queue("email_queue", durable=True)
    
    async def send_validation_email(self, token: Token, user_name: str):
        """Envia email de validação para a fila"""
        await self.connect()
        
        email_data = {
            "to_email": token.user_email,
            "user_name": user_name,
            "token": token.token,
            "expires_minutes": self.settings.token_expiration_minutes
        }
        
        message = aio_pika.Message(
            body=json.dumps(email_data).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        
        await self.channel.default_exchange.publish(
            message,
            routing_key="email_queue"
        )
        
        logger.info(f"Email enfileirado para {token.user_email}")
    
    async def close(self):
        """Fecha conexão"""
        if self.connection:
            await self.connection.close()