import streamlit as st
from typing import Dict, Any

class LandingPage:
    def __init__(self, container):
        self._container = container
        self._state_manager = container.state_manager()
        self._report_service = container.report_service()
    
    def render(self):
        """Render the landing page."""
        self._render_hero_section()
        self._render_features()
        self._render_about_section()
    
    def _render_hero_section(self):
        """Render the hero section with main image and call to action."""
        st.image(
            "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40",
            use_container_width=True
        )
        
        st.markdown("""
        ## Bem-vindo à IA do Empreendedor
        
        Uma plataforma que utiliza inteligência artificial para transformar dados em insights estratégicos, 
        simplificando a análise de mercado e monitorando indicadores essenciais para decisões mais seguras.
        """)
    
    def _render_features(self):
        """Render the features section with available report types."""
        st.markdown("### Conecte sua carteira digital para acessar:")
        
        report_types = self._report_service.get_report_types()
        cols = st.columns(len(report_types))
        
        for col, (report_id, report_info) in zip(cols, report_types.items()):
            with col:
                st.markdown(f"#### {report_info['name']}")
                st.markdown(report_info['description'])
        
        st.info("**Cada relatório custa apenas 1 Token Xperience.**")
    
    def _render_about_section(self):
        """Render the about section with project details."""
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