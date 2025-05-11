from abc import ABC, abstractmethod
from typing import Optional

class WalletInfo:
    def __init__(self, address: str, balance: float):
        self.address = address
        self.balance = balance

class IWalletService(ABC):
    @abstractmethod
    def connect(self, wallet_type: str) -> Optional[WalletInfo]:
        """Connect to a wallet and return wallet information if successful."""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect the current wallet."""
        pass
    
    @abstractmethod
    def check_balance(self, address: str) -> float:
        """Check the token balance for a given address."""
        pass 