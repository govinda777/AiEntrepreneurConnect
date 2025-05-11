from typing import Optional
from ...application.interfaces.i_wallet_service import IWalletService, WalletInfo
from web3 import Web3
import json

class MetaMaskService(IWalletService):
    def __init__(self):
        self.web3 = Web3(Web3.HTTPProvider('http://localhost:8545'))  # Update with your provider
        self.token_contract = None
        self._load_contract()
    
    def _load_contract(self):
        """Load the token contract."""
        try:
            with open('blockchain/build/contracts/XperienceToken.json') as f:
                contract_json = json.load(f)
                contract_address = contract_json['networks']['1']['address']  # Update with your network
                contract_abi = contract_json['abi']
                self.token_contract = self.web3.eth.contract(
                    address=contract_address,
                    abi=contract_abi
                )
        except Exception as e:
            print(f"Failed to load contract: {str(e)}")
    
    def connect(self, wallet_type: str) -> Optional[WalletInfo]:
        """Connect to MetaMask and return wallet information."""
        try:
            # In a real implementation, this would interact with the MetaMask API
            # For now, we'll simulate the connection
            accounts = self.web3.eth.accounts
            if not accounts:
                return None
                
            address = accounts[0]
            balance = self.check_balance(address)
            
            return WalletInfo(address=address, balance=balance)
            
        except Exception as e:
            print(f"Failed to connect to MetaMask: {str(e)}")
            return None
    
    def disconnect(self) -> None:
        """Disconnect from MetaMask."""
        # In a real implementation, this would clean up MetaMask connection
        pass
    
    def check_balance(self, address: str) -> float:
        """Check token balance for the given address."""
        try:
            if self.token_contract:
                balance = self.token_contract.functions.balanceOf(address).call()
                return float(balance) / (10 ** 18)  # Convert from wei to tokens
            return 0
        except Exception as e:
            print(f"Failed to check balance: {str(e)}")
            return 0 