from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from app.config.database import get_data
from app.services.brechas import build_dashboard, build_looker_csv
from app.schemas.brechas import DashboardBrechas

router = APIRouter(prefix="/api/brechas", tags=["Brechas"])


@router.get("/dashboard", response_model=DashboardBrechas)
def get_brechas_dashboard():
    df = get_data()
    return build_dashboard(df)


@router.get("/looker", response_class=PlainTextResponse)
def get_brechas_looker():
    df = get_data()
    return build_looker_csv(df)
