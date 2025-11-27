import sys
import os
from jinja2 import Template
from config.settings import get_settings

class TemplateService:
    def __init__(self):
        self.settings = get_settings()
        self.templates_dir = os.path.join(os.path.dirname(__file__), "../templates")
    
    def render_validation_email(self, user_name: str, token: str, expires_minutes: int) -> tuple[str, str]:
        """Renderiza template de email de validação retornando (html, text)"""
        template_path = os.path.join(self.templates_dir, "email_template.html")
        
        with open(template_path, 'r', encoding='utf-8') as file:
            template_content = file.read()
        
        template = Template(template_content)
        
        html_content = template.render(
            user_name=user_name,
            token=token,
            expires_minutes=expires_minutes,
            validation_url=f"{self.settings.api_base_url}/api/v1/validate-token/{token}"
        )
        
        # Gerar conteúdo texto
        text_content = f"""
            Defensoria Pública - Validação de Identidade

            Prezado(a) {user_name},

            Para continuar com seu atendimento, precisamos validar sua identidade.

            CLIQUE NO LINK ABAIXO PARA VALIDAR:
            {self.settings.api_base_url}/api/v1/validate-token/{token}

            OU utilize o código de verificação:
            {token}

            ⚠️ ATENÇÃO: Este código expira em {expires_minutes} minutos.
            Não compartilhe este código com ninguém.

            Se você não solicitou este atendimento, por favor ignore este email.

            Defensoria Pública - Sistema de Atendimento
            Este é um email automático. Por favor, não responda.
            """
        
        return html_content, text_content