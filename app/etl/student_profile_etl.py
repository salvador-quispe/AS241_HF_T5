"""
Student Profile ETL Module
Data transformations and queries for student profile BI dashboard
"""

import pandas as pd
from typing import Dict, List, Any, Optional
import logging

from app.config.database import get_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StudentProfileETL:
    """
    ETL processor for student profile data
    Contains all queries and transformations for BI analysis
    """
    
    def __init__(self, df: Optional[pd.DataFrame] = None):
        """Initialize ETL by loading data from database"""
        self.df = df.copy() if df is not None else get_data()
        self.total_students = len(self.df)
        logger.info(f"ETL initialized with {self.total_students} students")

    @staticmethod
    def _format_semester(value: Any) -> str:
        """Return a consistent semester label for API responses."""
        text = str(value).strip()
        if "semestre" in text.lower():
            return text

        if text.endswith(".0"):
            text = text[:-2]

        return f"{text}° Semestre"
    
    # ============================================
    # 1. KPI METRICS (Summary Cards)
    # ============================================
    
    def get_kpi_metrics(self) -> Dict[str, Any]:
        """
        Calculate main KPI metrics for dashboard cards
        
        Returns:
            Dict with KPI values in Spanish
        """
        # Age statistics
        avg_age = round(self.df['edad'].mean(), 1)
        min_age = int(self.df['edad'].min())
        max_age = int(self.df['edad'].max())
        
        # Academic risk: students with low job readiness (score <= 2)
        if 'preparado_ingresar_mercado_laboral' in self.df.columns:
            risk_count = len(self.df[self.df['preparado_ingresar_mercado_laboral'] <= 2])
        else:
            risk_count = 0
        
        if 'institucion_preparo_adecuadamente' in self.df.columns:
            institution_values = (
                self.df['institucion_preparo_adecuadamente']
                .astype(str)
                .str.strip()
                .str.lower()
            )
            satisfied = len(self.df[institution_values.isin(['si', 'sí'])])
            achievement = round((satisfied / self.total_students) * 100, 1)
        else:
            achievement = 0
        
        return {
            'total_estudiantes': self.total_students,
            'edad_promedio': avg_age,
            'edad_minima': min_age,
            'edad_maxima': max_age,
            'estudiantes_riesgo': int(risk_count),
            'logro_institucional': achievement
        }
    
    # ============================================
    # 2. JOB READINESS DISTRIBUTION
    # ============================================
    
    def get_job_readiness_distribution(self) -> List[Dict[str, Any]]:
        """
        Calculate job readiness distribution
        
        Returns:
            List with readiness levels
        """
        column = 'preparado_ingresar_mercado_laboral'
        readiness_counts = {
            'LOW': 0,
            'MEDIUM': 0,
            'HIGH': 0
        }
        
        if column not in self.df.columns:
            return [
                {'level': level, 'student_count': count, 'percentage': 0}
                for level, count in readiness_counts.items()
            ]
        
        for value in self.df[column].dropna():
            if value in [1, 2]:
                readiness_counts['LOW'] += 1
            elif value == 3:
                readiness_counts['MEDIUM'] += 1
            elif value in [4, 5]:
                readiness_counts['HIGH'] += 1
        
        result = []
        for level, count in readiness_counts.items():
            percentage = (count / self.total_students) * 100 if self.total_students else 0
            result.append({
                'level': level,
                'student_count': count,
                'percentage': round(percentage, 1)
            })
        
        return result
    
    # ============================================
    # 3. DISTRICT DISTRIBUTION
    # ============================================
    
    def get_district_distribution(self, top_n: int = 5) -> List[Dict[str, Any]]:
        """
        Calculate distribution by district of residence
        
        Args:
            top_n: Number of top districts to return
            
        Returns:
            List of district distribution data in Spanish
        """
        district_counts = self.df['distrito'].value_counts()
        total = len(self.df)
        
        results = []
        
        for idx, (district, count) in enumerate(district_counts.head(top_n).items()):
            percentage = (count / total) * 100
            
            results.append({
                'distrito': district,
                'cantidad_estudiantes': int(count),
                'porcentaje_participacion': round(percentage, 1)
            })
        
        return results
    
    # ============================================
    # 4. SEMESTER DISTRIBUTION
    # ============================================
    
    def get_semester_distribution(self) -> List[Dict[str, Any]]:
        """
        Calculate distribution by academic semester
        
        Returns:
            List of semester distribution data in Spanish
        """
        if 'semestre' in self.df.columns:
            semester_counts = self.df['semestre'].astype(str).str.strip().value_counts().sort_index()
        else:
            semester_counts = self.df['semestre'].value_counts().sort_index()
        
        total = len(self.df)
        
        results = []
        for semester, count in semester_counts.items():
            results.append({
                'semestre': self._format_semester(semester),
                'cantidad_estudiantes': int(count),
                'porcentaje': round((count / total) * 100, 1)
            })
        
        return results
    
    # ============================================
    # 5. AGE DISTRIBUTION (by ranges)
    # ============================================
    
    def get_age_distribution(self) -> List[Dict[str, Any]]:
        """
        Calculate age distribution by ranges
        
        Returns:
            List of age distribution data in Spanish
        """
        bins = [16, 19, 21, 23, 26, 100]
        labels = ['17-18', '19-20', '21-22', '23-25', '26+']
        
        self.df['rango_edad'] = pd.cut(self.df['edad'], bins=bins, labels=labels, right=False)
        age_counts = self.df['rango_edad'].value_counts()
        total = len(self.df)
        
        results = []
        for age_range in labels:
            count = age_counts.get(age_range, 0)
            results.append({
                'rango_edad': age_range,
                'cantidad_estudiantes': int(count),
                'porcentaje': round((count / total) * 100, 1)
            })
        
        return results
    
    # ============================================
    # 6. RISK BY SEMESTER
    # ============================================
    
    def get_risk_by_semester(self) -> List[Dict[str, Any]]:
        """
        Calculate students in academic risk by semester
        
        Returns:
            List of risk distribution by semester
        """
        if 'semestre' in self.df.columns:
            semestre_col = 'semestre'
        else:
            semestre_col = 'semestre'
        
        risk_data = []
        for semester in sorted(self.df[semestre_col].dropna().unique()):
            semester_df = self.df[self.df[semestre_col] == semester]
            if 'preparado_ingresar_mercado_laboral' in semester_df.columns:
                risk_count = len(semester_df[semester_df['preparado_ingresar_mercado_laboral'] <= 2])
                risk_data.append({
                    'semestre': self._format_semester(semester),
                    'total_estudiantes': len(semester_df),
                    'estudiantes_riesgo': risk_count,
                    'porcentaje_riesgo': round((risk_count / len(semester_df)) * 100, 1) if len(semester_df) > 0 else 0
                })
        return risk_data
    
    # ============================================
    # 7. AGE INSIGHT
    # ============================================
    
    def get_age_insight(self) -> str:
        """
        Generate insight about age distribution
        
        Returns:
            String with age distribution analysis
        """
        age_ranges = self.get_age_distribution()
        if not age_ranges:
            return ""

        most_common = max(age_ranges, key=lambda x: x['cantidad_estudiantes'])
        return (
            f"El rango de edad con mayor presencia es {most_common['rango_edad']} "
            f"con {most_common['porcentaje']}% de estudiantes."
        )
    
    # ============================================
    # 8. ANALYSIS INSIGHTS (Complete)
    # ============================================
    
    def generate_insights(self) -> str:
        """
        Generate business insights from the data
        
        Returns:
            String with complete analysis insights in Spanish
        """
        insights = []
        
        # Get top district insight
        district_data = self.get_district_distribution(top_n=1)
        if district_data:
            top_district = district_data[0]
            insights.append(
                f"El distrito con mayor concentración de estudiantes es {top_district['distrito']} "
                f"con {top_district['porcentaje_participacion']}% de participación."
            )
        
        # Check student distribution by semester
        semester_data = self.get_semester_distribution()
        if len(semester_data) > 0:
            most_populated = max(semester_data, key=lambda x: x['cantidad_estudiantes'])
            insights.append(
                f"El {most_populated['semestre']} concentra el "
                f"{most_populated['porcentaje']}% de estudiantes."
            )
        
        # Risk analysis
        kpi = self.get_kpi_metrics()
        if kpi['estudiantes_riesgo'] > 0:
            risk_percentage = round((kpi['estudiantes_riesgo'] / kpi['total_estudiantes']) * 100, 1)
            insights.append(f"Un {risk_percentage}% de estudiantes reporta baja preparación para ingresar al mercado laboral.")
        
        age_insight = self.get_age_insight()
        if age_insight:
            insights.append(age_insight)
        
        return " ".join(insights)
    
    # ============================================
    # 9. COMPLETE DASHBOARD DATA
    # ============================================
    
    def get_complete_dashboard_data(self) -> Dict[str, Any]:
        """
        Get all dashboard data in one consolidated dictionary
        
        Returns:
            Complete dashboard data ready for API response in Spanish
        """
        logger.info("Generating complete student profile dashboard data...")
        
        dashboard_data = {
            'indicadores_kpi': self.get_kpi_metrics(),
            'job_readiness_distribution': self.get_job_readiness_distribution(),
            'distribucion_distritos': self.get_district_distribution(top_n=6),
            'distribucion_semestres': self.get_semester_distribution(),
            'distribucion_edades': self.get_age_distribution(),
            'riesgo_por_semestre': self.get_risk_by_semester(),
            'analisis_insights': self.generate_insights()
        }
        
        logger.info("Dashboard data generation complete")
        return dashboard_data
    
    # ============================================
    # 10. EXPORT FUNCTIONS
    # ============================================
    
    def export_to_csv(self, filepath: str) -> None:
        """Export cleaned data to CSV for backup"""
        self.df.to_csv(filepath, index=False, encoding='utf-8-sig')
        logger.info(f"Data exported to {filepath}")
    
    def get_summary_statistics(self) -> pd.DataFrame:
        """Get summary statistics for all numeric columns"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        return self.df[numeric_cols].describe()
