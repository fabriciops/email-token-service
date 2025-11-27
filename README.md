# DefensorTokenValidator

Sistema de validação de identidade via token por email para a Defensoria Pública.

## Configuração Rápida

1. Clone o repositório
2. Copie `.env.example` para `.env` e configure as variáveis
3. Execute: `docker-compose up -d`

## Endpoints da API

### Receber dados do Typebot

POST /api/v1/receive-user-data
Content-Type: application/json
X-API-Hash: your-hash-key

{
"nome": "Fabricio",
"email": "fabricio@example.com",
"telefone": "21998143283",
"cpf": "14675156711"
}
text


### Validar Token

GET /api/v1/validate-token/{token}
text


## Acesso aos Serviços

- API: http://localhost:8000
- MongoDB: localhost:27017
- RabbitMQ Management: http://localhost:15672 (admin/securepassword123)

## Deploy AWS

Execute o script de deploy:

```bash
chmod +x deploy.sh
./deploy.sh
```

```bash

### `deploy.sh`
```bash
#!/bin/bash

# DefensorTokenValidator - Script de Deploy AWS
echo "Iniciando deploy do DefensorTokenValidator..."

# Atualizar sistema
sudo apt-get update
sudo apt-get upgrade -y

# Instalar Docker
if ! command -v docker &> /dev/null; then
    echo "Instalando Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
fi

# Instalar Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "Instalando Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Criar diretório do projeto
PROJECT_DIR="/opt/defensor-token-validator"
sudo mkdir -p $PROJECT_DIR
sudo chown $USER:$USER $PROJECT_DIR

# Copiar arquivos do projeto (assumindo que estão no mesmo diretório)
cp -r ./* $PROJECT_DIR/
cd $PROJECT_DIR

# Configurar environment
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Configure as variáveis no arquivo .env antes de continuar!"
    exit 1
fi

# Build e deploy
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Verificar status
echo "Aguardando serviços inicializarem..."
sleep 30

# Health check
echo "Verificando saúde dos serviços..."
docker-compose ps

echo "Deploy concluído!"
echo "API disponível em: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8000"
echo "RabbitMQ Management: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):15672"
```

# Fazer uma nova requisição para testar
curl -X POST http://localhost:8000/api/v1/receive-user-data \
  -H "Content-Type: application/json" \
  -H "X-API-Hash: XXXXXXXXXXXXXXX" \
  -d '{
    "nome": "Teste Final",
    "email": "teste-final@example.com", 
    "telefone": "21997776655",
    "cpf": "11122233344"
  }'

# Verificar se a mensagem chegou no RabbitMQ
docker exec defensor_rabbitmq rabbitmqctl list_queues name messages messages_ready

# Ver logs do email_service
docker-compose logs -f email_service