import sys
import os
from jinja2 import Template
from config.settings import get_settings

class TemplateService:
    def __init__(self):
        self.settings = get_settings()
        self.templates_dir = os.path.join(os.path.dirname(__file__), "../templates")
    
    def render_validation_email(self, user_name: str, token: str, expires_minutes: int) -> str:
        """Renderiza template de email de validação"""
        template_path = os.path.join(self.templates_dir, "email_template.html")
        
        with open(template_path, 'r', encoding='utf-8') as file:
            template_content = file.read()
        
        template = Template(template_content)
        
        return template.render(
            user_name=user_name,
            token=token,
            expires_minutes=expires_minutes,
            validation_url=f"{self.settings.api_base_url}/api/v1/validate-token/{token}"
        )