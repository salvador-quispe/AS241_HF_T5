"""
Routes package
Centralized route registration
"""

from app.api.controllers.student_profile_controller import router as student_profile_router

# List of all routers to be included in main app
routers = [
    student_profile_router,
]

__all__ = ['routers']