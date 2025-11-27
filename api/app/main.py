from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.config.settings import get_settings
from app.routers import users, tokens
from app.utils.security import verify_api_hash
import logging
import os

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Iniciando DefensorTokenValidator API")
    yield
    # Shutdown
    logger.info("Encerrando DefensorTokenValidator API")

# Crie a app PRIMEIRO
app = FastAPI(
    title="DefensorTokenValidator API",
    description="Sistema de validação de identidade da Defensoria Pública",
    version="1.0.0",
    lifespan=lifespan
)

# Configure templates DEPOIS de criar a app
templates = Jinja2Templates(directory="app/templates")

# Configure arquivos estáticos DEPOIS de criar a app
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de autenticação para endpoints protegidos
async def verify_api_key(x_api_hash: str = Header(...)):
    if not verify_api_hash(x_api_hash):
        raise HTTPException(status_code=401, detail="API Hash inválido")
    return True

# Incluir routers DEPOIS de criar a app
app.include_router(
    users.router, 
    prefix="/api/v1", 
    tags=["users"],
    dependencies=[Depends(verify_api_key)]
)
app.include_router(
    tokens.router, 
    prefix="/api/v1", 
    tags=["tokens"]
)

@app.get("/")
async def root():
    return {"message": "DefensorTokenValidator API - Defensoria Pública"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "DefensorTokenValidator API"}