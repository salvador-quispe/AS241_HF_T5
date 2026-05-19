from fastapi import APIRouter
from app.api.controllers.student_profile_controller import router as perfil_router

api_router = APIRouter()
api_router.include_router(perfil_router)