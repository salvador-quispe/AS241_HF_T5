from fastapi import APIRouter
from app.api.controllers.habilidades_blandas_controller import router as blandas_router

api_router = APIRouter()
api_router.include_router(blandas_router)