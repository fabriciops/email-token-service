import aio_pika
from app.config.settings import get_settings
import logging

logger = logging.getLogger(__name__)

async def get_rabbitmq_connection():
    """Retorna conexão com RabbitMQ"""
    settings = get_settings()
    return await aio_pika.connect_robust(settings.rabbitmq_url)