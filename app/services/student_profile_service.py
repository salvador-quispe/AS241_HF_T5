"""
Student Profile Service
Business logic layer for student profile module
"""

from typing import Dict, Any, Optional
from datetime import datetime
import logging

from app.repositories.student_profile_repository import StudentProfileRepository

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StudentProfileService:
    """
    Service layer for student profile business logic
    Orchestrates data access and applies business rules
    """
    
    def __init__(self, google_sheets_url: str):
        """
        Initialize service with repository
        
        Args:
            google_sheets_url: CSV export URL from Google Sheets
        """
        self.repository = StudentProfileRepository(google_sheets_url)
        self.last_response_time = None
    
    def get_dashboard_data(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Get complete dashboard data with metadata
        
        Args:
            force_refresh: Force refresh from source
            
        Returns:
            Standardized response with dashboard data and metadata
        """
        start_time = datetime.now()
        
        try:
            # Get data from repository
            dashboard_data = self.repository.get_dashboard_data(force_refresh)
            
            if dashboard_data is None:
                return self._error_response("No data available", start_time)
            
            # Add metadata
            response = {
                'success': True,
                'module': 'student_profile',
                'data': dashboard_data,
                'metadata': {
                    'last_updated': self.repository.connector.get_last_update(),
                    'response_time_ms': int((datetime.now() - start_time).total_seconds() * 1000),
                    'data_source': 'google_sheets',
                    'cache_used': not force_refresh and self.repository._cache_valid
                }
            }
            
            self.last_response_time = response['metadata']['response_time_ms']
            logger.info(f"Dashboard data retrieved in {response['metadata']['response_time_ms']}ms")
            
            return response
            
        except Exception as e:
            logger.error(f"Error getting dashboard data: {str(e)}")
            return self._error_response(str(e), start_time)
    
    def get_kpi_metrics(self, force_refresh: bool = False) -> Dict[str, Any]:
        """Get only KPI metrics"""
        try:
            kpi_data = self.repository.get_kpi_metrics(force_refresh)
            
            if kpi_data is None:
                return self._error_response("No KPI data available")
            
            return {
                'success': True,
                'module': 'student_profile',
                'data': {'kpi_metrics': kpi_data},
                'metadata': {
                    'last_updated': self.repository.connector.get_last_update(),
                    'endpoint': 'kpi_metrics'
                }
            }
        except Exception as e:
            return self._error_response(str(e))
    
    def get_career_distribution(self, force_refresh: bool = False) -> Dict[str, Any]:
        """Get career distribution data"""
        try:
            career_data = self.repository.get_career_distribution(force_refresh)
            
            if career_data is None:
                return self._error_response("No career distribution data available")
            
            return {
                'success': True,
                'module': 'student_profile',
                'data': {'career_distribution': career_data},
                'metadata': {
                    'last_updated': self.repository.connector.get_last_update(),
                    'endpoint': 'career_distribution'
                }
            }
        except Exception as e:
            return self._error_response(str(e))
    
    def get_district_distribution(self, top_n: int = 5, force_refresh: bool = False) -> Dict[str, Any]:
        """Get district distribution data"""
        try:
            district_data = self.repository.get_district_distribution(top_n, force_refresh)
            
            if district_data is None:
                return self._error_response("No district distribution data available")
            
            return {
                'success': True,
                'module': 'student_profile',
                'data': {'district_distribution': district_data},
                'metadata': {
                    'last_updated': self.repository.connector.get_last_update(),
                    'endpoint': 'district_distribution',
                    'top_n': top_n
                }
            }
        except Exception as e:
            return self._error_response(str(e))
    
    def refresh_data(self) -> Dict[str, Any]:
        """Force refresh data from source"""
        self.repository.invalidate_cache()
        return self.get_dashboard_data(force_refresh=True)
    
    def _error_response(self, message: str, start_time: datetime = None) -> Dict[str, Any]:
        """Generate standardized error response"""
        response = {
            'success': False,
            'module': 'student_profile',
            'error': message,
            'metadata': {
                'timestamp': datetime.now().isoformat()
            }
        }
        
        if start_time:
            response['metadata']['response_time_ms'] = int((datetime.now() - start_time).total_seconds() * 1000)
        
        return response
    

# Add this method to StudentProfileService class

def get_semester_distribution(self, force_refresh: bool = False) -> Dict[str, Any]:
    """Get semester distribution data"""
    try:
        etl = self.repository.load_data(force_refresh)
        
        if etl is None:
            return self._error_response("No data available")
        
        semester_data = etl.get_semester_distribution()
        
        return {
            'success': True,
            'module': 'student_profile',
            'data': {'semester_distribution': semester_data},
            'metadata': {
                'last_updated': self.repository.connector.get_last_update(),
                'endpoint': 'semester_distribution'
            }
        }
    except Exception as e:
        return self._error_response(str(e))