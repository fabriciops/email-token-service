import smtplib
from email.mime.text import MIMEText as MimeText
from email.mime.multipart import MIMEMultipart as MimeMultipart
from email.utils import formatdate, make_msgid
from config.settings import get_settings
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class EmailSender:
    def __init__(self):
        self.settings = get_settings()
    
    def send_email(self, to_email: str, subject: str, html_content: str, text_content: str = None):
        """Envia email via SMTP com headers completos"""
        try:
            # Criar mensagem multipart
            message = MimeMultipart("alternative")
            
            # HEADERS ESSENCIAIS ANTI-SPAM
            message['Date'] = formatdate(localtime=True)
            message['Message-ID'] = make_msgid(domain='defensoria-publica.org')
            message['From'] = self.settings.from_email
            message['To'] = to_email
            message['Subject'] = subject
            message['MIME-Version'] = '1.0'
            message['X-Mailer'] = 'DefensoriaPublica/1.0'
            message['X-Priority'] = '3'
            message['X-MS-Exchange-Organization-AuthAs'] = 'Internal'
            message['X-MS-Exchange-Organization-AuthSource'] = 'defensoria-publica.org'
            
            # Se não fornecer conteúdo texto, criar versão simplificada do HTML
            if not text_content:
                text_content = self._html_to_text(html_content)
            
            # Parte em texto puro (OBRIGATÓRIO anti-spam)
            text_part = MimeText(text_content, 'plain', 'utf-8')
            message.attach(text_part)
            
            # Parte HTML
            html_part = MimeText(html_content, 'html', 'utf-8')
            message.attach(html_part)
            
            logger.info(f"Enviando email para: {to_email}")
            logger.info(f"Headers: Date={message['Date']}, Message-ID={message['Message-ID']}")
            
            # Mailtrap na porta 2525 usa SMTP + STARTTLS
            with smtplib.SMTP(self.settings.smtp_server, self.settings.smtp_port, timeout=30) as server:
                server.starttls()
                server.login(self.settings.smtp_username, self.settings.smtp_password)
                server.send_message(message)
                logger.info(f"✅ Email enviado com sucesso para: {to_email}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao enviar email para {to_email}: {e}")
            raise
    
    def _html_to_text(self, html_content: str) -> str:
        """Converte HTML para texto simples para versão text/plain"""
        import re
        
        # Remove tags HTML
        text = re.sub(r'<[^>]+>', '', html_content)
        
        # Remove múltiplos espaços e quebras
        text = re.sub(r'\s+', ' ', text)
        
        # Cria versão legível
        lines = [
            "Defensoria Pública - Validação de Identidade",
            "",
            "Para continuar com seu agendamento, valide sua identidade clicando no link abaixo:",
            "",
            f"Link de validação: {self._extract_validation_url(html_content)}",
            "",
            "Ou utilize o código de verificação abaixo:",
            f"Código: {self._extract_token(html_content)}",
            "",
            "Atenção: Este código expira em 15 minutos.",
            "Não compartilhe este código com ninguém.",
            "",
            "Se você não solicitou este atendimento, por favor ignore este email.",
            "",
            "Defensoria Pública - Sistema de Atendimento",
            "Este é um email automático. Por favor, não responda."
        ]
        
        return '\n'.join(lines)
    
    def _extract_validation_url(self, html_content: str) -> str:
        """Extrai URL de validação do HTML"""
        import re
        match = re.search(r'href="([^"]*validate-token[^"]*)"', html_content)
        return match.group(1) if match else "URL não disponível"
    
    def _extract_token(self, html_content: str) -> str:
        """Extrai token do HTML"""
        import re
        match = re.search(r'<div class="token">([^<]+)</div>', html_content)
        return match.group(1) if match else "TOKEN não disponível"