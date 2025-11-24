from app.config.settings import get_settings
import hmac

def verify_api_hash(received_hash: str) -> bool:
    """Valida se o hash recebido é igual ao API_HASH_KEY do ambiente"""
    settings = get_settings()
    return hmac.compare_digest(settings.api_hash_key, received_hash)
