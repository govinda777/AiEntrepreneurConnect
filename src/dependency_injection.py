from infrastructure.persistence.session_state_manager import SessionStateManager
from infrastructure.services.metamask_service import MetaMaskService
from infrastructure.services.report_service import ReportService
from application.use_cases.generate_report_use_case import GenerateReportUseCase
from application.use_cases.wallet_connection_use_case import WalletConnectionUseCase

class Container:
    """Dependency Injection Container"""
    
    def __init__(self):
        self._instances = {}
    
    def state_manager(self):
        """Get the state manager instance."""
        if 'state_manager' not in self._instances:
            self._instances['state_manager'] = SessionStateManager()
        return self._instances['state_manager']
    
    def wallet_service(self):
        """Get the wallet service instance."""
        if 'wallet_service' not in self._instances:
            self._instances['wallet_service'] = MetaMaskService()
        return self._instances['wallet_service']
    
    def report_service(self):
        """Get the report service instance."""
        if 'report_service' not in self._instances:
            self._instances['report_service'] = ReportService()
        return self._instances['report_service']
    
    def wallet_connection_use_case(self):
        """Get the wallet connection use case instance."""
        if 'wallet_connection_use_case' not in self._instances:
            self._instances['wallet_connection_use_case'] = WalletConnectionUseCase(
                self.wallet_service(),
                self.state_manager()
            )
        return self._instances['wallet_connection_use_case']
    
    def generate_report_use_case(self):
        """Get the generate report use case instance."""
        if 'generate_report_use_case' not in self._instances:
            self._instances['generate_report_use_case'] = GenerateReportUseCase(
                self.report_service(),
                self.state_manager()
            )
        return self._instances['generate_report_use_case'] 