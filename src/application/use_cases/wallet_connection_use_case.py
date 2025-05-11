from ..interfaces.i_wallet_service import IWalletService, WalletInfo
from ..interfaces.i_state_manager import IStateManager

class WalletConnectionUseCase:
    def __init__(self, wallet_service: IWalletService, state_manager: IStateManager):
        self._wallet_service = wallet_service
        self._state_manager = state_manager
    
    def connect(self, wallet_type: str) -> bool:
        """
        Connect to a wallet and update application state.
        
        Args:
            wallet_type: Type of wallet to connect to ('metamask' or 'walletconnect')
            
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            wallet_info = self._wallet_service.connect(wallet_type)
            
            if wallet_info:
                self._state_manager.set('wallet_connected', True)
                self._state_manager.set('wallet_address', wallet_info.address)
                self._state_manager.set('token_balance', wallet_info.balance)
                return True
                
            return False
            
        except Exception as e:
            print(f"Failed to connect wallet: {str(e)}")
            return False
    
    def disconnect(self) -> None:
        """Disconnect wallet and clear related state."""
        try:
            self._wallet_service.disconnect()
        finally:
            self._state_manager.set('wallet_connected', False)
            self._state_manager.set('wallet_address', '')
            self._state_manager.set('token_balance', 0) 