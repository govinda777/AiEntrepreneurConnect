from typing import Dict, Any
from ..interfaces.i_report_service import IReportService, Report
from ..interfaces.i_state_manager import IStateManager

class GenerateReportUseCase:
    def __init__(self, report_service: IReportService, state_manager: IStateManager):
        self._report_service = report_service
        self._state_manager = state_manager
    
    def execute(self, report_type: str, form_data: Dict[str, Any]) -> Report:
        """
        Generate a report and handle token deduction.
        
        Args:
            report_type: Type of report to generate
            form_data: Form data for report generation
            
        Returns:
            Generated report
            
        Raises:
            ValueError: If insufficient tokens or invalid form data
        """
        # Validate token balance
        token_balance = self._state_manager.get('token_balance', 0)
        if token_balance < 1:
            raise ValueError("Insufficient tokens. Each report costs 1 Token Xperience.")
            
        # Validate form data
        if not self._report_service.validate_form_data(report_type, form_data):
            raise ValueError("Invalid form data provided.")
            
        # Generate report
        report = self._report_service.generate_report(report_type, form_data)
        
        # Deduct token and update state
        self._state_manager.set('token_balance', token_balance - 1)
        
        # Add report to history
        reports = self._state_manager.get('reports', [])
        reports.append(report)
        self._state_manager.set('reports', reports)
        
        return report 