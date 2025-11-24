from app.config.settings import get_settings
import hmac

class SecurityService:
    def __init__(self):
        self.settings = get_settings()
    
    def validate_api_hash(self, received_hash: str) -> bool:
        """Valida se o hash recebido é igual ao API_HASH_KEY do ambiente"""
        return hmac.compare_digest(self.settings.api_hash_key, received_hash)