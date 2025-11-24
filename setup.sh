#!/bin/bash

echo "=== CONFIGURAÇÃO DO DEFENSOR TOKEN VALIDATOR ==="

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python3 não encontrado. Instalando..."
    sudo apt update
    sudo apt install -y python3
fi

# Função para gerar senha
generate_password() {
    python3 -c "import secrets, string; print(''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16)))"
}

# Função para gerar chave
generate_key() {
    python3 -c "import secrets; print(secrets.token_urlsafe($1))"
}

# Gerar chaves
echo "Gerando chaves seguras..."
SECRET_KEY=$(generate_key 64)
API_HASH_KEY=$(generate_key 32)
MONGO_PASSWORD=$(generate_password)
RABBITMQ_PASSWORD=$(generate_password)

# Criar arquivo .env
cat > .env << EOF
# MongoDB
MONGO_ROOT_USERNAME=admin
MONGO_ROOT_PASSWORD=${MONGO_PASSWORD}
MONGO_DB_NAME=defensortokenvalidator
MONGODB_URL=mongodb://admin:${MONGO_PASSWORD}@mongodb:27017/defensortokenvalidator?authSource=admin

# RabbitMQ
RABBITMQ_USER=admin
RABBITMQ_PASS=${RABBITMQ_PASSWORD}
RABBITMQ_URL=amqp://admin:${RABBITMQ_PASSWORD}@rabbitmq:5672/

# API
SECRET_KEY=${SECRET_KEY}
API_HASH_KEY=${API_HASH_KEY}

# Email Service (CONFIGURE ESTES DADOS)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=seu-email@gmail.com
SMTP_PASSWORD=sua-app-password
FROM_EMAIL=defensoria-publica@example.com
API_BASE_URL=http://localhost:8000

# Application
TOKEN_EXPIRATION_MINUTES=15
EOF

echo "Arquivo .env criado com sucesso!"
echo
echo "IMPORTANTE: Configure os dados de email no arquivo .env:"
echo " - SMTP_USERNAME"
echo " - SMTP_PASSWORD" 
echo " - FROM_EMAIL"
echo
echo "Chaves geradas:"
echo "SECRET_KEY: ${SECRET_KEY:0:20}..."
echo "API_HASH_KEY: ${API_HASH_KEY:0:20}..."
echo "MongoDB Password: ${MONGO_PASSWORD}"
echo "RabbitMQ Password: ${RABBITMQ_PASSWORD}"