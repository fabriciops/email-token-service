import sys
import os
import smtplib
from email.mime.text import MIMEText as MimeText
from email.mime.multipart import MIMEMultipart as MimeMultipart
from config.settings import get_settings
import logging

logger = logging.getLogger(__name__)

class EmailSender:
    def __init__(self):
        self.settings = get_settings()
    
    def send_email(self, to_email: str, subject: str, html_content: str):
        """Envia email via SMTP"""
        try:
            # Criar mensagem
            message = MimeMultipart()
            message['From'] = self.settings.from_email
            message['To'] = to_email
            message['Subject'] = subject
            message.attach(MimeText(html_content, 'html'))
            
            logger.info(f"Enviando email para: {to_email}")
            logger.info(f"Usando servidor: {self.settings.smtp_server}:{self.settings.smtp_port}")
            
            # Mailtrap na porta 2525 usa SMTP + STARTTLS
            with smtplib.SMTP(self.settings.smtp_server, self.settings.smtp_port, timeout=30) as server:
                server.starttls()  # Upgrade para TLS
                server.login(self.settings.smtp_username, self.settings.smtp_password)
                server.send_message(message)
                logger.info(f"Email enviado com sucesso para: {to_email}")
            
        except Exception as e:
            logger.error(f"Erro ao enviar email para {to_email}: {e}")
            raise