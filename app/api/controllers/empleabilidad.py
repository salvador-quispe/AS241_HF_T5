from fastapi import APIRouter
from app.config.database import get_data
from app.services.empleabilidad import build_dashboard
from app.schemas.empleabilidad import DashboardEmpleabilidad

router = APIRouter(prefix="/api/empleabilidad", tags=["Empleabilidad"])


@router.get("/dashboard", response_model=DashboardEmpleabilidad)
def get_empleabilidad_dashboard():
    df = get_data()
    return build_dashboard(df)
