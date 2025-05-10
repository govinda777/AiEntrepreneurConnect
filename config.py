from pathlib import Path
from typing import Optional
import os
from dotenv import load_dotenv

class EnvironmentManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        # Carrega as variáveis de ambiente do arquivo .env
        env_path = Path('.env')
        load_dotenv(dotenv_path=env_path)
        
        self._initialized = True
    
    @staticmethod
    def get(key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Obtém uma variável de ambiente.
        
        Args:
            key: Nome da variável de ambiente
            default: Valor padrão caso a variável não exista
            
        Returns:
            Valor da variável de ambiente ou o valor padrão
        """
        return os.getenv(key, default)
    
    @staticmethod
    def require(key: str) -> str:
        """
        Obtém uma variável de ambiente obrigatória.
        
        Args:
            key: Nome da variável de ambiente
            
        Returns:
            Valor da variável de ambiente
            
        Raises:
            ValueError: Se a variável de ambiente não existir
        """
        value = os.getenv(key)
        if value is None:
            raise ValueError(f"Variável de ambiente obrigatória não encontrada: {key}")
        return value
    
    @staticmethod
    def set(key: str, value: str) -> None:
        """
        Define uma variável de ambiente.
        
        Args:
            key: Nome da variável de ambiente
            value: Valor a ser definido
        """
        os.environ[key] = value 