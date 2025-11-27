import sys
import os
import pika
import json
import logging
from services.email_sender import EmailSender
from services.template_service import TemplateService
from config.settings import get_settings
\
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailConsumer:
    def __init__(self):
        self.settings = get_settings()
        self.email_sender = EmailSender()
        self.template_service = TemplateService()
    
    def process_email(self, email_data: dict):
        """Processa e envia email"""
        try:
            logger.info(f"Processando email para: {email_data['to_email']}")
            
            # Renderizar template (agora retorna HTML e Texto)
            html_content, text_content = self.template_service.render_validation_email(
                user_name=email_data["user_name"],
                token=email_data["token"],
                expires_minutes=email_data["expires_minutes"]
            )
            
            # Enviar email com ambas as versões
            self.email_sender.send_email(
                to_email=email_data["to_email"],
                subject="Validação de Identidade - Defensoria Pública",
                html_content=html_content,
                text_content=text_content
            )
            
            logger.info(f"✅ Email enviado com sucesso para: {email_data['to_email']}")
            
        except Exception as e:
            logger.error(f"❌ Erro no processamento do email: {e}")
            raise
    
    def consume_emails(self):
        """Consome mensagens da fila de emails"""
        try:
            logger.info("Conectando ao RabbitMQ...")
            connection = pika.BlockingConnection(
                pika.URLParameters(self.settings.rabbitmq_url)
            )
            channel = connection.channel()
            channel.queue_declare(queue='email_queue', durable=True)
            
            def callback(ch, method, properties, body):
                try:
                    email_data = json.loads(body.decode())
                    logger.info(f"📨 Nova mensagem recebida para: {email_data['to_email']}")
                    self.process_email(email_data)
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    logger.info(f"✅ Mensagem processada: {email_data['to_email']}")
                except Exception as e:
                    logger.error(f"❌ Erro ao processar mensagem: {e}")
                    # Não fazer acknowledge para reprocessamento
            
            channel.basic_consume(queue='email_queue', on_message_callback=callback)
            logger.info("🚀 Email Consumer iniciado - Aguardando mensagens...")
            channel.start_consuming()
            
        except Exception as e:
            logger.error(f"❌ Erro no consumer: {e}")
            raise

if __name__ == "__main__":
    consumer = EmailConsumer()
    consumer.consume_emails()