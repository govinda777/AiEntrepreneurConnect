import streamlit as st
import time
import json
from web3 import Web3
from eth_account import Account
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações da blockchain
ARBITRUM_RPC_URL = os.getenv('ARBITRUM_RPC_URL', 'https://arb1.arbitrum.io/rpc')
TOKEN_ADDRESS = os.getenv('TOKEN_ADDRESS', '')
PAYMENT_SYSTEM_ADDRESS = os.getenv('PAYMENT_SYSTEM_ADDRESS', '')

# Inicializar Web3
w3 = Web3(Web3.HTTPProvider(ARBITRUM_RPC_URL))

# Carregar ABIs
def load_contract_abi(contract_name):
    try:
        with open(f'blockchain/artifacts/contracts/{contract_name}.sol/{contract_name}.json') as f:
            contract_json = json.load(f)
            return contract_json['abi']
    except Exception as e:
        st.error(f"Erro ao carregar ABI do contrato {contract_name}: {str(e)}")
        return None

# Inicializar contratos
def init_contracts():
    token_abi = load_contract_abi('AiEntrepreneurToken')
    payment_system_abi = load_contract_abi('ReportPaymentSystem')
    
    if token_abi and payment_system_abi:
        token_contract = w3.eth.contract(address=TOKEN_ADDRESS, abi=token_abi)
        payment_system_contract = w3.eth.contract(address=PAYMENT_SYSTEM_ADDRESS, abi=payment_system_abi)
        return token_contract, payment_system_contract
    return None, None

def connect_wallet(wallet_type):
    """
    Simula a conexão de uma carteira e retorna um endereço
    """
    # Endereço simulado
    wallet_address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
    
    # Salvar informações na sessão
    st.session_state.wallet_connected = True
    st.session_state.wallet_address = wallet_address
    st.session_state.token_balance = 5  # Começa com 5 tokens
    
    st.success(f"Conectado em modo de simulação via {wallet_type.capitalize()}!")
    return True

def disconnect_wallet():
    """Desconectar a carteira"""
    st.session_state.wallet_connected = False
    st.session_state.wallet_address = ""
    st.session_state.token_balance = 0
    st.session_state.token_contract = None
    st.session_state.payment_system_contract = None
    
    st.success("Carteira desconectada com sucesso!")
    return True

def fetch_token_balance():
    """
    Buscar saldo de tokens da carteira conectada
    """
    try:
        if not st.session_state.wallet_connected or not st.session_state.token_contract:
            return 0
        
        balance = st.session_state.token_contract.functions.balanceOf(
            st.session_state.wallet_address
        ).call()
        
        # Converter de wei para tokens
        token_balance = balance / 10**18
        st.session_state.token_balance = token_balance
        
        return token_balance
        
    except Exception as e:
        st.error(f"Erro ao buscar saldo de tokens: {str(e)}")
        return 0

def check_token_balance():
    """Verificar se usuário tem tokens suficientes para uma transação"""
    if not st.session_state.wallet_connected:
        return False
    
    try:
        report_cost = st.session_state.payment_system_contract.functions.getReportCost().call()
        current_balance = st.session_state.token_contract.functions.balanceOf(
            st.session_state.wallet_address
        ).call()
        
        return current_balance >= report_cost
        
    except Exception as e:
        st.error(f"Erro ao verificar saldo: {str(e)}")
        return False

def request_report():
    """
    Solicitar um novo relatório via smart contract
    """
    try:
        if not st.session_state.wallet_connected:
            st.error("Carteira não conectada")
            return False
            
        # Verificar saldo
        if not check_token_balance():
            st.error("Saldo insuficiente de tokens")
            return False
            
        # Aprovar gasto de tokens
        report_cost = st.session_state.payment_system_contract.functions.getReportCost().call()
        approve_tx = st.session_state.token_contract.functions.approve(
            st.session_state.payment_system_contract.address,
            report_cost
        ).build_transaction({
            'from': st.session_state.wallet_address,
            'nonce': w3.eth.get_transaction_count(st.session_state.wallet_address),
        })
        
        # Assinar e enviar transação de aprovação
        signed_approve_tx = w3.eth.account.sign_transaction(approve_tx, os.getenv('PRIVATE_KEY'))
        approve_tx_hash = w3.eth.send_raw_transaction(signed_approve_tx.rawTransaction)
        w3.eth.wait_for_transaction_receipt(approve_tx_hash)
        
        # Solicitar relatório
        report_tx = st.session_state.payment_system_contract.functions.requestReport().build_transaction({
            'from': st.session_state.wallet_address,
            'nonce': w3.eth.get_transaction_count(st.session_state.wallet_address),
        })
        
        # Assinar e enviar transação do relatório
        signed_report_tx = w3.eth.account.sign_transaction(report_tx, os.getenv('PRIVATE_KEY'))
        report_tx_hash = w3.eth.send_raw_transaction(signed_report_tx.rawTransaction)
        receipt = w3.eth.wait_for_transaction_receipt(report_tx_hash)
        
        # Atualizar saldo
        fetch_token_balance()
        
        return True
        
    except Exception as e:
        st.error(f"Erro ao solicitar relatório: {str(e)}")
        return False

def format_wallet_address(address):
    """Formatar endereço da carteira para exibição"""
    if address and len(address) > 10:
        return f"{address[:6]}...{address[-4:]}"
    return address
