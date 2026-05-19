"""
Student Profile Controller
Handles HTTP requests and returns responses for student profile module
"""

from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Query, status

from app.services.student_profile_service import StudentProfileService
from app.schemas.student_profile_schema import APIResponseSchema

# Create router
router = APIRouter(prefix="/api/v1/student-profile", tags=["Student Profile"])

# Initialize service (in production, use dependency injection)
# Replace with your actual Google Sheets CSV URL
GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR_ql_51qQMBj27nihHNfGCi9QsllcXgyKoRJomooOkApcQgcHt-y3XdoFtCWPlBsumJ9vvjklsZ8gs/pub?output=csv"

service = StudentProfileService(GOOGLE_SHEETS_URL)


@router.get("/dashboard", response_model=APIResponseSchema)
async def get_dashboard(
    force_refresh: bool = Query(False, description="Force refresh data from Google Sheets")
) -> Dict[str, Any]:
    """
    Get complete student profile dashboard data
    
    - **force_refresh**: Set to true to bypass cache and fetch fresh data
    """
    response = service.get_dashboard_data(force_refresh=force_refresh)
    
    if not response['success']:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=response['error'])
    
    return response


@router.get("/kpi", response_model=APIResponseSchema)
async def get_kpi_metrics(
    force_refresh: bool = Query(False, description="Force refresh data")
) -> Dict[str, Any]:
    """
    Get only KPI metrics (summary cards)
    """
    response = service.get_kpi_metrics(force_refresh=force_refresh)
    
    if not response['success']:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=response['error'])
    
    return response


@router.get("/career-distribution", response_model=APIResponseSchema)
async def get_career_distribution(
    force_refresh: bool = Query(False, description="Force refresh data")
) -> Dict[str, Any]:
    """
    Get career distribution by gender
    
    Returns distribution of students across careers with gender breakdown
    """
    response = service.get_career_distribution(force_refresh=force_refresh)
    
    if not response['success']:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=response['error'])
    
    return response


@router.get("/district-distribution", response_model=APIResponseSchema)
async def get_district_distribution(
    top_n: int = Query(5, ge=1, le=20, description="Number of top districts to return"),
    force_refresh: bool = Query(False, description="Force refresh data")
) -> Dict[str, Any]:
    """
    Get district distribution of students
    
    - **top_n**: Number of top districts to show (default: 5)
    """
    response = service.get_district_distribution(top_n=top_n, force_refresh=force_refresh)
    
    if not response['success']:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=response['error'])
    
    return response


@router.get("/semester-distribution", response_model=APIResponseSchema)
async def get_semester_distribution(
    force_refresh: bool = Query(False, description="Force refresh data")
) -> Dict[str, Any]:
    """
    Get distribution of students by academic semester
    """
    response = service.get_semester_distribution(force_refresh=force_refresh)
    
    if not response['success']:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=response['error'])
    
    return response


@router.get("/age-distribution", response_model=APIResponseSchema)
async def get_age_distribution(
    force_refresh: bool = Query(False, description="Force refresh data")
) -> Dict[str, Any]:
    """
    Get age distribution by age ranges
    """
    # This method needs to be added to the service
    # For now, we get it from dashboard data
    dashboard_response = service.get_dashboard_data(force_refresh=force_refresh)
    
    if not dashboard_response['success']:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=dashboard_response['error'])
    
    # Extract age distribution from dashboard data
    age_distribution = dashboard_response['data'].get('age_distribution', [])
    
    return {
        'success': True,
        'module': 'student_profile',
        'data': {'age_distribution': age_distribution},
        'metadata': dashboard_response.get('metadata', {})
    }


@router.post("/refresh", response_model=APIResponseSchema)
async def refresh_data() -> Dict[str, Any]:
    """
    Force refresh data from Google Sheets (clears cache)
    """
    response = service.refresh_data()
    
    if not response['success']:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=response['error'])
    
    return response


@router.get("/health", response_model=APIResponseSchema)
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint to verify API is working
    """
    return {
        'success': True,
        'module': 'student_profile',
        'data': {'status': 'healthy'},
        'metadata': {
            'timestamp': str(__import__('datetime').datetime.now()),
            'service': 'student_profile_api'
        }
    }