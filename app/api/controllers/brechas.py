from fastapi import APIRouter
from app.config.database import get_data
from app.services.brechas import build_dashboard
from app.schemas.brechas import DashboardBrechas

router = APIRouter(prefix="/api/brechas", tags=["Brechas"])


@router.get("/dashboard", response_model=DashboardBrechas)
def get_brechas_dashboard():
    df = get_data()
    return build_dashboard(df)
