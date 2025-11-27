import hmac
import hashlib

def generate_api_hash(api_hash_key: str):
    """Gera o hash que deve ser enviado no header X-API-Hash"""
    hash_obj = hmac.new(
        api_hash_key.encode(),
        b"api_validation",  # Mesmo salt usado na validação
        hashlib.sha256
    )
    return hash_obj.hexdigest()
  
API_HASH_KEY = "xgUvUNiKEmE1Zv_lz-kNdRy4041VN7ZMnI0U4hOPoyg"

hash_correto = "xgUvUNiKEmE1Zv_lz-kNdRy4041VN7ZMnI0U4hOPoyg"

print(f"Hash correto para usar no header: {hash_correto}")
print(f"\nComando curl:")
print(f"""
curl -X POST http://localhost:8000/api/v1/receive-user-data \\
  -H "Content-Type: application/json" \\
  -H "X-API-Hash: {hash_correto}" \\
  -d '{{
    "nome": "João Silva",
    "email": "teste@example.com", 
    "telefone": "21999999999",
    "cpf": "12345678900"
  }}'
""")