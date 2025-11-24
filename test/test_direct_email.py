import asyncio
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
email_service_path = os.path.join(project_root, 'email_service', 'app')
sys.path.insert(0, email_service_path)

from services.email_sender import EmailSender
from config.settings import get_settings

async def test_direct_email():
    try:
        settings = get_settings()
        email_sender = EmailSender()
        
        print("=== TESTE DIRETO DE EMAIL ===")
        print(f"SMTP Server: {settings.smtp_server}:{settings.smtp_port}")
        print(f"From: {settings.from_email}")
        
        # Testar envio direto
        await email_sender.send_email(
            to_email="test@example.com",
            subject="TESTE - Defensoria Pública",
            html_content="<h1>Teste de Email</h1><p>Este é um teste do sistema.</p>"
        )
        
        print("✅ Email enviado com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")

if __name__ == "__main__":
    asyncio.run(test_direct_email())