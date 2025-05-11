from abc import ABC, abstractmethod
from typing import Dict, Any

class Report:
    def __init__(self, report_type: str, content: Dict[str, Any], metadata: Dict[str, Any]):
        self.report_type = report_type
        self.content = content
        self.metadata = metadata
        self.created_at = metadata.get('created_at')

class IReportService(ABC):
    @abstractmethod
    def generate_report(self, report_type: str, form_data: Dict[str, Any]) -> Report:
        """Generate a report based on the type and form data."""
        pass
    
    @abstractmethod
    def get_report_types(self) -> Dict[str, Dict[str, Any]]:
        """Get available report types and their metadata."""
        pass
    
    @abstractmethod
    def validate_form_data(self, report_type: str, form_data: Dict[str, Any]) -> bool:
        """Validate form data for a specific report type."""
        pass 