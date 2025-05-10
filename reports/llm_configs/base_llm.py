from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class LLMConfig:
    """Configuração base para LLMs"""
    model_name: str
    temperature: float
    max_tokens: int
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0

class ReportLLM(ABC):
    """
    Classe base para configuração e gerenciamento dos LLMs usados
    nos relatórios.
    """
    
    def __init__(self, config: LLMConfig):
        self.config = config
        
    @abstractmethod
    def generate_analysis(self, prompts: Dict[str, str], data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gera a análise do relatório usando o LLM configurado.
        Deve retornar um dicionário com os resultados da análise.
        """
        pass
        
    @abstractmethod
    def generate_recommendations(self, prompts: Dict[str, str], analysis: Dict[str, Any]) -> list:
        """
        Gera recomendações baseadas na análise usando o LLM configurado.
        Deve retornar uma lista de recomendações.
        """
        pass
        
    @abstractmethod
    def validate_output(self, output: Dict[str, Any]) -> bool:
        """
        Valida se a saída do LLM está no formato esperado e
        contém todas as informações necessárias.
        """
        pass
        
    def get_completion(self, prompt: str, **kwargs) -> Optional[str]:
        """
        Método auxiliar para obter uma completion do LLM.
        Pode ser sobrescrito para implementar retry logic, error handling, etc.
        """
        try:
            # Implementação específica de cada LLM deve ser feita nas classes filhas
            return None
        except Exception as e:
            print(f"Error getting completion: {e}")
            return None 