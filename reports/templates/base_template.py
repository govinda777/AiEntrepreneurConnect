from abc import ABC, abstractmethod
from typing import Dict, Any

class ReportTemplate(ABC):
    """
    Template base para todos os relatórios.
    Define a estrutura comum que todos os relatórios devem seguir.
    """
    
    def __init__(self, report_id: str, generated_date: str):
        self.report_id = report_id
        self.generated_date = generated_date
        
    @abstractmethod
    def format_executive_summary(self, data: Dict[str, Any]) -> str:
        """Formata o sumário executivo do relatório"""
        pass
        
    @abstractmethod
    def format_main_content(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Formata o conteúdo principal do relatório"""
        pass
        
    @abstractmethod
    def format_recommendations(self, data: Dict[str, Any]) -> list:
        """Formata as recomendações do relatório"""
        pass
        
    @abstractmethod
    def format_visualizations(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Formata as visualizações do relatório"""
        pass
        
    def generate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gera o relatório completo usando os dados fornecidos.
        Este método não deve ser sobrescrito pelas classes filhas.
        """
        return {
            "id": self.report_id,
            "generated_date": self.generated_date,
            "executive_summary": self.format_executive_summary(data),
            "content": self.format_main_content(data),
            "recommendations": self.format_recommendations(data),
            "visualizations": self.format_visualizations(data),
            "raw_data": data
        } 