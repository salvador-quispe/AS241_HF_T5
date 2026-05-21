"""
AS241_HF_T5 - Habilidades Blandas BI Dashboard
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import api_router
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AS241_HF_T5 - Habilidades Blandas API",
    description="Backend para análisis de encuestas - Módulo de Habilidades Blandas",
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
        "app": "AS241_HF_T5 - Habilidades Blandas API",
        "version": "1.0.0",
        "modulo": "Habilidades Blandas",
        "endpoints": {
            "dashboard": "/api/habilidades-blandas/dashboard",
            "kpi": "/api/habilidades-blandas/kpi",
            "promedios": "/api/habilidades-blandas/promedios",
            "mejorar": "/api/habilidades-blandas/mejorar",
            "satisfaccion": "/api/habilidades-blandas/satisfaccion",
            "interes": "/api/habilidades-blandas/interes",
            "insights": "/api/habilidades-blandas/insights",
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