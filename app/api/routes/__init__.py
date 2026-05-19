from fastapi import APIRouter
from app.api.controllers.brechas import router as brechas_router
from app.api.controllers.empleabilidad import router as empleabilidad_router
from app.api.controllers.etl import router as etl_router

api_router = APIRouter()
api_router.include_router(brechas_router)
api_router.include_router(empleabilidad_router)
api_router.include_router(etl_router)
