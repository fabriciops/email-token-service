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

# Copiar arquivos do projeto
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

# Testar API
echo "Testando API..."
curl -f http://localhost:8000/health || echo "API não respondeu"

echo "Deploy concluído!"
echo "API disponível em: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8000"
echo "RabbitMQ Management: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):15673"
echo "MongoDB: localhost:27018"