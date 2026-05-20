"""
API Routes Configuration
"""

from fastapi import APIRouter
from app.api.controllers.digital_skills_controller import router as digital_skills_router

api_router = APIRouter()

# Include all module routers
api_router.include_router(digital_skills_router)