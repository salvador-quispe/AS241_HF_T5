from fastapi import APIRouter
from app.api.controllers.habilidades_blandas_controller import router as blandas_router
from app.api.controllers.habilidades_tecnicas_controller import router as tecnicas_router

api_router = APIRouter()
api_router.include_router(blandas_router)
api_router.include_router(tecnicas_router)