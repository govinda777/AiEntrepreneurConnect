import streamlit as st
from dependency_injection import Container
from presentation.pages.landing_page import LandingPage
from presentation.pages.dashboard_page import DashboardPage
from presentation.pages.report_form_page import ReportFormPage
from presentation.pages.report_view_page import ReportViewPage

def setup_page_config():
    """Configure the Streamlit page."""
    st.set_page_config(
        page_title="IA do Empreendedor",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

def initialize_state(container):
    """Initialize application state if not already initialized."""
    state_manager = container.state_manager()
    
    if not state_manager.get('initialized'):
        state_manager.set('wallet_connected', False)
        state_manager.set('wallet_address', '')
        state_manager.set('token_balance', 0)
        state_manager.set('reports', [])
        state_manager.set('current_page', 'home')
        state_manager.set('selected_report_type', None)
        state_manager.set('form_data', {})
        state_manager.set('initialized', True)

def main():
    """Main application entry point."""
    # Setup dependency injection
    container = Container()
    
    # Configure page
    setup_page_config()
    
    # Initialize state
    initialize_state(container)
    
    # Get current state
    state_manager = container.state_manager()
    wallet_connected = state_manager.get('wallet_connected')
    current_page = state_manager.get('current_page')
    
    # Render header with wallet connection
    render_header(container)
    
    # Render main content
    if not wallet_connected:
        LandingPage(container).render()
    else:
        pages = {
            'home': DashboardPage(container),
            'form': ReportFormPage(container),
            'report': ReportViewPage(container)
        }
        
        current_page_component = pages.get(current_page)
        if current_page_component:
            current_page_component.render()
        else:
            st.error("Invalid page")
            state_manager.set('current_page', 'home')
            st.rerun()

def render_header(container):
    """Render the application header with wallet connection."""
    state_manager = container.state_manager()
    wallet_use_case = container.wallet_connection_use_case()
    
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.title("IA do Empreendedor")
            st.subheader("Transformando dados em estratégia para seu negócio")
            
        with col2:
            if state_manager.get('wallet_connected'):
                wallet_address = state_manager.get('wallet_address')
                token_balance = state_manager.get('token_balance')
                
                st.success(f"Conectado: {wallet_address[:6]}...{wallet_address[-4:]}")
                st.info(f"Tokens: {token_balance}")
                
                if st.button("Desconectar"):
                    wallet_use_case.disconnect()
                    st.rerun()
            else:
                connect_col1, connect_col2 = st.columns(2)
                with connect_col1:
                    if st.button("Metamask"):
                        if wallet_use_case.connect("metamask"):
                            st.rerun()
                with connect_col2:
                    if st.button("WalletConnect"):
                        if wallet_use_case.connect("walletconnect"):
                            st.rerun()

if __name__ == "__main__":
    main() 