"""
AS241_HF_T5 - Digital Skills BI Dashboard
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import api_router
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AS241_HF_T5 - Habilidades Digitales API",
    description="Backend para análisis de encuestas - Módulo Habilidades Digitales",
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
        "app": "AS241_HF_T5 - Habilidades Digitales API",
        "version": "1.0.0",
        "modulo": "Habilidades Digitales",
        "endpoints": {
            "dashboard": "/api/habilidades-digitales/dashboard",
            "kpi": "/api/habilidades-digitales/kpi",
            "herramientas_ofimaticas": "/api/habilidades-digitales/herramientas-ofimaticas",
            "plataformas_lenguajes": "/api/habilidades-digitales/plataformas-lenguajes",
            "estudiantes": "/api/habilidades-digitales/estudiantes",
            "conclusiones": "/api/habilidades-digitales/conclusiones",
            "acciones_recomendadas": "/api/habilidades-digitales/acciones-recomendadas",
            "proxima_evaluacion": "/api/habilidades-digitales/proxima-evaluacion",
        },
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
