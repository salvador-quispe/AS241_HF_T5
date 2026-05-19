from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import api_router
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AS241_HF_T5 - Encuestas API",
    description="Backend para análisis de encuestas — Módulos Brechas y Empleabilidad (Google Sheets + Pandas)",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
def root():
    return {
        "app": "AS241_HF_T5 - Encuestas API",
        "version": "1.0.0",
        "fuente": "Google Sheets (caché en memoria)",
        "endpoints": {
            "brechas": "/api/brechas/dashboard",
            "empleabilidad": "/api/empleabilidad/dashboard",
            "etl": "POST /api/etl/load",
        },
    }
