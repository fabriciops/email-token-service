// Script de inicialização do MongoDB
db = db.getSiblingDB('defensortokenvalidator');

// Criar coleções
db.createCollection('users');
db.createCollection('tokens');

// Criar índices
db.users.createIndex({ "email": 1 }, { unique: true });
db.users.createIndex({ "cpf": 1 }, { unique: true });
db.tokens.createIndex({ "token": 1 }, { unique: true });
db.tokens.createIndex({ "created_at": 1 }, { expireAfterSeconds: 3600 }); // Expira após 1 hora

// Inserir dados iniciais (opcional)
print("Banco de dados DefensorTokenValidator inicializado com sucesso!");