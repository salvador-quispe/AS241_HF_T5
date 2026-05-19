"""
AS241_HF_T5 - Student Profile BI Dashboard
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import api_router
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AS241_HF_T5 - Perfil Estudiante API",
    description="Backend para análisis de encuestas - Módulo Perfil del Estudiante",
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
        "app": "AS241_HF_T5 - Perfil Estudiante API",
        "version": "1.0.0",
        "modulo": "Perfil del Estudiante",
        "endpoints": {
            "dashboard": "/api/perfil-estudiante/dashboard",
            "kpi": "/api/perfil-estudiante/kpi",
            "genero": "/api/perfil-estudiante/genero",
            "carreras": "/api/perfil-estudiante/carreras",
            "distritos": "/api/perfil-estudiante/distritos",
            "semestres": "/api/perfil-estudiante/semestres",
            "edades": "/api/perfil-estudiante/edades",
            "riesgo": "/api/perfil-estudiante/riesgo",
            "insights": "/api/perfil-estudiante/insights",
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