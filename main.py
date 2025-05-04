import streamlit as st
import time
import pandas as pd
from PIL import Image
import base64
from io import BytesIO
import os

# Import custom modules
from wallet_connector import connect_wallet, check_token_balance, disconnect_wallet
from dashboard import render_dashboard
from forms import (
    render_business_map_form, 
    render_blue_ocean_form, 
    render_seo_form
)
from report_generator import generate_report, generate_sample_reports
from utils import load_css, set_page_config, display_report

# Page configuration
set_page_config()

# Initialize session state variables if they don't exist
if 'wallet_connected' not in st.session_state:
    st.session_state.wallet_connected = False
if 'wallet_address' not in st.session_state:
    st.session_state.wallet_address = ""
if 'token_balance' not in st.session_state:
    st.session_state.token_balance = 0
if 'reports' not in st.session_state:
    st.session_state.reports = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"
if 'selected_report_type' not in st.session_state:
    st.session_state.selected_report_type = None
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

# Main app
def main():
    # Header section with logo and wallet connection
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.title("IA do Empreendedor")
            st.subheader("Transformando dados em estratégia para seu negócio")
        with col2:
            if st.session_state.wallet_connected:
                st.success(f"Conectado: {st.session_state.wallet_address[:6]}...{st.session_state.wallet_address[-4:]}")
                st.info(f"Tokens: {st.session_state.token_balance}")
                if st.button("Desconectar"):
                    disconnect_wallet()
            else:
                connect_col1, connect_col2 = st.columns(2)
                with connect_col1:
                    if st.button("Metamask"):
                        connect_wallet("metamask")
                with connect_col2:
                    if st.button("WalletConnect"):
                        connect_wallet("walletconnect")

    # Main content
    if not st.session_state.wallet_connected:
        show_landing_page()
    else:
        if st.session_state.current_page == "home":
            show_dashboard()
        elif st.session_state.current_page == "form":
            show_report_form()
        elif st.session_state.current_page == "report":
            show_report()

def show_landing_page():
    """Display the landing page for non-connected users"""
    st.image("https://images.unsplash.com/photo-1454165804606-c3d57bc86b40", use_column_width=True)
    
    st.markdown("""
    ## Bem-vindo à IA do Empreendedor
    
    Uma plataforma que utiliza inteligência artificial para transformar dados em insights estratégicos, 
    simplificando a análise de mercado e monitorando indicadores essenciais para decisões mais seguras.
    
    ### Conecte sua carteira digital para acessar:
    
    - 🗺️ **Mapa do Seu Negócio**: Um dashboard que mapeia a situação atual da empresa e identifica áreas para crescimento.
    - 🌊 **Relatório Xperience**: Utiliza o método Blue Ocean para explorar novos mercados e orientar decisões estratégicas.
    - 🔍 **Relatório SEO**: Otimiza sua presença online, monitorando tráfego e indicadores-chave de performance.
    
    **Cada relatório custa apenas 1 Token Xperience.**
    """)
    
    with st.expander("Sobre o Projeto Xperience"):
        st.markdown("""
        A "IA do Empreendedor" foi desenvolvida para empoderar empreendedores, essa ferramenta utiliza inteligência 
        artificial para transformar dados em insights estratégicos, simplificando a análise de mercado e monitorando 
        indicadores essenciais para decisões mais seguras.
        
        #### Objetivos:
        - Automatizar análises de mercado detalhadas e identificar oportunidades emergentes.
        - Gerar insights preditivos que orientem decisões estratégicas e operacionais.
        - Facilitar o acesso a informações críticas para o sucesso do negócio.
        """)

def show_dashboard():
    """Display the main dashboard when user is connected"""
    # Navigation tabs
    tab1, tab2 = st.tabs(["Gerar Novo Relatório", "Meus Relatórios"])
    
    with tab1:
        st.header("Selecione o tipo de relatório")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.image("https://images.unsplash.com/photo-1532102522784-9e4d4d9a533c", use_column_width=True)
            st.subheader("Mapa do Seu Negócio")
            st.write("Visualize a situação atual da sua empresa e identifique áreas para crescimento.")
            if st.button("Gerar Mapa", key="btn_map"):
                st.session_state.selected_report_type = "business_map"
                st.session_state.current_page = "form"
                st.rerun()
                
        with col2:
            st.image("https://images.unsplash.com/photo-1529119368496-2dfda6ec2804", use_column_width=True)
            st.subheader("Relatório Xperience")
            st.write("Estratégia Blue Ocean para explorar novos mercados e orientar decisões estratégicas.")
            if st.button("Gerar Xperience", key="btn_xperience"):
                st.session_state.selected_report_type = "blue_ocean"
                st.session_state.current_page = "form"
                st.rerun()
                
        with col3:
            st.image("https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3", use_column_width=True)
            st.subheader("Relatório SEO")
            st.write("Otimize sua presença online, monitorando tráfego e indicadores-chave de performance.")
            if st.button("Gerar SEO", key="btn_seo"):
                st.session_state.selected_report_type = "seo"
                st.session_state.current_page = "form"
                st.rerun()
    
    with tab2:
        st.header("Meus Relatórios")
        
        if not st.session_state.reports:
            st.info("Você ainda não gerou nenhum relatório. Gere seu primeiro relatório na aba 'Gerar Novo Relatório'.")
        else:
            render_dashboard()

def show_report_form():
    """Display the appropriate report form based on user selection"""
    # Back button
    if st.button("← Voltar para o Dashboard"):
        st.session_state.current_page = "home"
        st.session_state.selected_report_type = None
        st.rerun()
    
    # Form title
    if st.session_state.selected_report_type == "business_map":
        st.header("Mapa do Seu Negócio")
        form_submitted = render_business_map_form()
    elif st.session_state.selected_report_type == "blue_ocean":
        st.header("Relatório Xperience (Blue Ocean)")
        form_submitted = render_blue_ocean_form()
    elif st.session_state.selected_report_type == "seo":
        st.header("Relatório SEO")
        form_submitted = render_seo_form()
    else:
        st.error("Tipo de relatório inválido.")
        return
    
    # Handle form submission
    if form_submitted:
        # Check token balance
        if st.session_state.token_balance < 1:
            st.error("Saldo de tokens insuficiente. Cada relatório custa 1 Token Xperience.")
            return
        
        # Process the report generation
        with st.spinner("Gerando seu relatório... Por favor, aguarde."):
            # Simulate processing time (in a real app, this would be the actual API processing)
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.05)
                progress_bar.progress(i + 1)
            
            # Generate the report and update token balance
            report = generate_report(
                report_type=st.session_state.selected_report_type,
                form_data=st.session_state.form_data
            )
            
            # Add report to session state
            st.session_state.reports.append(report)
            
            # Deduct token
            st.session_state.token_balance -= 1
            
            # Navigate to report view
            st.session_state.current_page = "report"
            st.rerun()

def show_report():
    """Display the most recently generated report"""
    # Back button
    if st.button("← Voltar para o Dashboard"):
        st.session_state.current_page = "home"
        st.rerun()
    
    # Show the most recent report
    if st.session_state.reports:
        latest_report = st.session_state.reports[-1]
        display_report(latest_report)
    else:
        st.error("Nenhum relatório encontrado.")
        st.session_state.current_page = "home"
        st.rerun()

if __name__ == "__main__":
    # Generate sample reports for testing
    if 'initialized' not in st.session_state:
        generate_sample_reports()
        st.session_state.initialized = True
    
    # Run the app
    main()
