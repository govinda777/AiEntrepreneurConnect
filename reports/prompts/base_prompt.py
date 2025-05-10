from abc import ABC, abstractmethod
from typing import Dict, Any

class ReportPrompt(ABC):
    """
    Classe base para todos os prompts de relatório.
    Define a estrutura e formatação dos prompts para cada tipo de relatório.
    """
    
    def __init__(self):
        self.system_prompt = self.get_system_prompt()
        
    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        Retorna o prompt do sistema que define o comportamento base do LLM
        para este tipo de relatório.
        """
        pass
        
    @abstractmethod
    def format_user_prompt(self, data: Dict[str, Any]) -> str:
        """
        Formata os dados do usuário em um prompt específico para este
        tipo de relatório.
        """
        pass
        
    @abstractmethod
    def format_analysis_prompt(self, data: Dict[str, Any]) -> str:
        """
        Formata um prompt específico para análise dos dados e geração
        de insights.
        """
        pass
        
    @abstractmethod
    def format_recommendations_prompt(self, data: Dict[str, Any]) -> str:
        """
        Formata um prompt específico para geração de recomendações
        baseadas nos dados e análises.
        """
        pass
        
    def get_prompts(self, data: Dict[str, Any]) -> Dict[str, str]:
        """
        Retorna todos os prompts necessários para gerar o relatório.
        Este método não deve ser sobrescrito pelas classes filhas.
        """
        return {
            "system": self.system_prompt,
            "user": self.format_user_prompt(data),
            "analysis": self.format_analysis_prompt(data),
            "recommendations": self.format_recommendations_prompt(data)
        } 