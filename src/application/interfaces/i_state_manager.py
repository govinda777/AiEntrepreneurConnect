from abc import ABC, abstractmethod
from typing import Any, Optional

class IStateManager(ABC):
    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the state."""
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """Set a value in the state."""
        pass
    
    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete a value from the state."""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear all state."""
        pass 