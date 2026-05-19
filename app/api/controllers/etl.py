from fastapi import APIRouter
from app.etl.loader import run_etl
from pydantic import BaseModel

router = APIRouter(prefix="/api/etl", tags=["ETL"])


class EtlResponse(BaseModel):
    status: str
    records_loaded: int


@router.get("/load", response_model=EtlResponse)
def load_survey_data_get():
    count = run_etl()
    return EtlResponse(status="ok", records_loaded=count)


@router.post("/load", response_model=EtlResponse)
def load_survey_data_post():
    count = run_etl()
    return EtlResponse(status="ok", records_loaded=count)
