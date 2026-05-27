"""
Student Profile Data Models
Data classes for type-safe data handling
"""

from dataclasses import dataclass
from typing import List


@dataclass
class KPIMetrics:
    """KPI metrics for summary cards"""
    total_students: int
    average_age: float
    min_age: int
    max_age: int
    academic_risk_count: int
    institutional_achievement: float
    
    def to_dict(self) -> dict:
        return {
            'total_students': self.total_students,
            'average_age': self.average_age,
            'min_age': self.min_age,
            'max_age': self.max_age,
            'academic_risk_count': self.academic_risk_count,
            'institutional_achievement': self.institutional_achievement
        }


@dataclass
class JobReadinessDistribution:
    """Job readiness distribution"""
    level: str
    student_count: int
    percentage: float
    
    def to_dict(self) -> dict:
        return {
            'level': self.level,
            'student_count': self.student_count,
            'percentage': round(self.percentage, 1)
        }


@dataclass
class DistrictData:
    """District participation data"""
    district: str
    student_count: int
    participation_percentage: float
    
    def to_dict(self) -> dict:
        return {
            'district': self.district,
            'student_count': self.student_count,
            'participation_percentage': round(self.participation_percentage, 1)
        }


@dataclass
class SemesterDistribution:
    """Distribution by semester"""
    semester: str
    student_count: int
    percentage: float
    
    def to_dict(self) -> dict:
        return {
            'semester': self.semester,
            'student_count': self.student_count,
            'percentage': round(self.percentage, 1)
        }


@dataclass
class AgeDistribution:
    """Age distribution data"""
    age_range: str
    student_count: int
    percentage: float
    
    def to_dict(self) -> dict:
        return {
            'age_range': self.age_range,
            'student_count': self.student_count,
            'percentage': round(self.percentage, 1)
        }


@dataclass
class StudentProfileDashboard:
    """Complete dashboard data for student profile module"""
    kpi_metrics: KPIMetrics
    job_readiness_distribution: List[JobReadinessDistribution]
    district_data: List[DistrictData]
    semester_distribution: List[SemesterDistribution]
    age_distribution: List[AgeDistribution]
    last_updated: str
    analysis_insights: str
    
    def to_dict(self) -> dict:
        return {
            'kpi_metrics': self.kpi_metrics.to_dict(),
            'job_readiness_distribution': [
                item.to_dict() for item in self.job_readiness_distribution
            ],
            'district_data': [d.to_dict() for d in self.district_data],
            'semester_distribution': [s.to_dict() for s in self.semester_distribution],
            'age_distribution': [a.to_dict() for a in self.age_distribution],
            'last_updated': self.last_updated,
            'analysis_insights': self.analysis_insights
        }
