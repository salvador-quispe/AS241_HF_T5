"""
Student Profile Schemas
Pydantic models for request/response validation
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


# ============================================
# KPI Metrics Schema
# ============================================

class KPIMetricsSchema(BaseModel):
    total_students: int = Field(..., description="Total number of surveyed students")
    growth_percentage: float = Field(..., description="Growth compared to previous cycle")
    average_age: float = Field(..., description="Average age of students")
    min_age: int = Field(..., description="Minimum age")
    max_age: int = Field(..., description="Maximum age")
    academic_risk_count: int = Field(..., description="Students requiring academic support")
    institutional_target: int = Field(..., description="Institutional satisfaction target (%)")
    institutional_achievement: float = Field(..., description="Current achievement (%)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_students": 842,
                "growth_percentage": 4.2,
                "average_age": 20.4,
                "min_age": 17,
                "max_age": 26,
                "academic_risk_count": 34,
                "institutional_target": 95,
                "institutional_achievement": 92.0
            }
        }


# ============================================
# Career Distribution Schema
# ============================================

class CareerDistributionSchema(BaseModel):
    career: str = Field(..., description="Career name")
    male_count: int = Field(..., description="Number of male students")
    female_count: int = Field(..., description="Number of female students")
    total: int = Field(..., description="Total students")
    percentage: float = Field(..., description="Percentage of total")
    
    class Config:
        json_schema_extra = {
            "example": {
                "career": "Programa de Análisis de Sistemas Empresariales",
                "male_count": 340,
                "female_count": 172,
                "total": 512,
                "percentage": 60.8
            }
        }


# ============================================
# District Distribution Schema
# ============================================

class DistrictDistributionSchema(BaseModel):
    district: str = Field(..., description="District name")
    province: str = Field(..., description="Province name")
    student_count: int = Field(..., description="Number of students")
    participation_percentage: float = Field(..., description="Participation percentage")
    
    class Config:
        json_schema_extra = {
            "example": {
                "district": "San Vicente de Cañete",
                "province": "Cañete",
                "student_count": 324,
                "participation_percentage": 18.5
            }
        }


# ============================================
# Semester Distribution Schema
# ============================================

class SemesterDistributionSchema(BaseModel):
    semester: int = Field(..., description="Semester number (1, 5, 6)")
    student_count: int = Field(..., description="Number of students")
    percentage: float = Field(..., description="Percentage of total")
    
    class Config:
        json_schema_extra = {
            "example": {
                "semester": 1,
                "student_count": 32,
                "percentage": 47.1
            }
        }


# ============================================
# Age Distribution Schema
# ============================================

class AgeDistributionSchema(BaseModel):
    age_range: str = Field(..., description="Age range (e.g., '17-18', '19-20')")
    student_count: int = Field(..., description="Number of students")
    percentage: float = Field(..., description="Percentage of total")
    
    class Config:
        json_schema_extra = {
            "example": {
                "age_range": "17-18",
                "student_count": 35,
                "percentage": 51.5
            }
        }


# ============================================
# Complete Dashboard Schema
# ============================================

class StudentProfileDashboardSchema(BaseModel):
    kpi_metrics: KPIMetricsSchema
    career_distribution: List[CareerDistributionSchema]
    district_distribution: List[DistrictDistributionSchema]
    semester_distribution: List[SemesterDistributionSchema]
    age_distribution: List[AgeDistributionSchema]
    analysis_insights: str = Field(..., description="Business insights from data analysis")
    
    class Config:
        json_schema_extra = {
            "example": {
                "analysis_insights": "Se detecta una tendencia de crecimiento en el distrito de San Vicente de Cañete. Se recomienda evaluar rutas de transporte institucional."
            }
        }


# ============================================
# API Response Schema
# ============================================

class APIResponseSchema(BaseModel):
    success: bool = Field(..., description="Request success status")
    module: str = Field(..., description="Module name")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    error: Optional[str] = Field(None, description="Error message if any")
    metadata: Dict[str, Any] = Field(..., description="Response metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "module": "student_profile",
                "data": {},
                "metadata": {
                    "last_updated": "2026-05-19 15:30:00",
                    "response_time_ms": 245
                }
            }
        }