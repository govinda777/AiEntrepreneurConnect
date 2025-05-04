import streamlit as st
import re
from utils import validate_url

def render_business_map_form():
    """Render form for Business Map report"""
    st.subheader("Preencha os dados sobre seu negócio")
    
    with st.form("business_map_form"):
        # Business information
        business_name = st.text_input("Nome da empresa", max_chars=100)
        
        col1, col2 = st.columns(2)
        with col1:
            industry = st.selectbox(
                "Setor de atuação",
                options=[
                    "Tecnologia",
                    "Saúde",
                    "Educação",
                    "Varejo",
                    "Finanças",
                    "Alimentação",
                    "Manufatura",
                    "Serviços",
                    "Outro"
                ]
            )
            
            if industry == "Outro":
                industry = st.text_input("Especifique o setor")
        
        with col2:
            business_model = st.selectbox(
                "Modelo de negócio",
                options=[
                    "SaaS",
                    "E-commerce",
                    "Marketplace",
                    "Assinatura",
                    "Freemium",
                    "Consultoria",
                    "Produto físico",
                    "Outro"
                ]
            )
            
            if business_model == "Outro":
                business_model = st.text_input("Especifique o modelo de negócio")
        
        # Business metrics
        col1, col2 = st.columns(2)
        with col1:
            monthly_revenue = st.number_input(
                "Faturamento mensal médio (R$)",
                min_value=0,
                value=50000,
                step=10000,
                format="%d"
            )
        
        with col2:
            employees = st.number_input(
                "Número de colaboradores",
                min_value=1,
                value=10,
                step=1,
                format="%d"
            )
        
        # Products and audience
        main_products = st.text_area(
            "Principais produtos/serviços (separados por vírgula)",
            placeholder="Ex: Software de gestão, Consultoria, Treinamentos"
        )
        
        target_audience = st.text_area(
            "Público-alvo",
            placeholder="Ex: Pequenas e médias empresas do setor de saúde"
        )
        
        # Competition
        competitors = st.text_area(
            "Principais concorrentes (separados por vírgula)",
            placeholder="Ex: Empresa A, Empresa B, Empresa C"
        )
        
        # Marketing
        col1, col2 = st.columns(2)
        with col1:
            marketing_channels = st.multiselect(
                "Canais de marketing utilizados",
                options=[
                    "Redes Sociais",
                    "Email Marketing",
                    "SEO/Google",
                    "Anúncios pagos",
                    "Marketing de conteúdo",
                    "Eventos/Feiras",
                    "Parcerias",
                    "Indicações"
                ]
            )
        
        with col2:
            growth_stage = st.selectbox(
                "Estágio de crescimento da empresa",
                options=[
                    "Início/MVP",
                    "Validação",
                    "Crescimento",
                    "Escala",
                    "Maturidade"
                ]
            )
        
        # Submit button
        submitted = st.form_submit_button("Gerar Mapa do Seu Negócio")
        
        if submitted:
            # Validate inputs
            if not business_name:
                st.error("Por favor, informe o nome da empresa.")
                return False
            
            if not main_products:
                st.error("Por favor, informe os principais produtos/serviços.")
                return False
            
            if not target_audience:
                st.error("Por favor, informe o público-alvo.")
                return False
            
            # Store data in session state
            st.session_state.form_data = {
                'business_name': business_name,
                'industry': industry,
                'business_model': business_model,
                'monthly_revenue': monthly_revenue,
                'employees': employees,
                'main_products': main_products,
                'target_audience': target_audience,
                'competitors': competitors,
                'marketing_channels': marketing_channels,
                'growth_stage': growth_stage
            }
            
            return True
    
    return False

def render_blue_ocean_form():
    """Render form for Blue Ocean Strategy report"""
    st.subheader("Informe os dados para gerar seu Relatório Xperience (Blue Ocean)")
    
    with st.form("blue_ocean_form"):
        # Basic information
        business_name = st.text_input("Nome da empresa", max_chars=100)
        
        # Products and services
        products_services = st.text_area(
            "Produtos/Serviços atuais",
            placeholder="Ex: Software de gestão financeira, Consultoria especializada"
        )
        
        # Competitors
        competitors = st.text_area(
            "Principais concorrentes (separados por vírgula)",
            placeholder="Ex: Empresa A, Empresa B, Empresa C"
        )
        
        # Target audience
        target_customers = st.text_area(
            "Cliente-alvo",
            placeholder="Ex: Pequenas e médias empresas do setor de tecnologia"
        )
        
        # Differentials
        differentials = st.text_area(
            "Diferenciais competitivos atuais",
            placeholder="Ex: Preço acessível, Atendimento personalizado, Tecnologia proprietária"
        )
        
        # Business challenges
        challenges = st.text_area(
            "Principais desafios do negócio",
            placeholder="Ex: Alta competição por preço, Dificuldade de aquisição de clientes"
        )
        
        # Goals
        goals = st.text_area(
            "Objetivos estratégicos",
            placeholder="Ex: Expandir para novos mercados, Aumentar margem de lucro"
        )
        
        # Resources
        col1, col2 = st.columns(2)
        with col1:
            strengths = st.text_area(
                "Principais pontos fortes",
                placeholder="Ex: Equipe qualificada, Tecnologia proprietária"
            )
        
        with col2:
            limitations = st.text_area(
                "Principais limitações",
                placeholder="Ex: Orçamento limitado, Equipe pequena"
            )
        
        # Submit button
        submitted = st.form_submit_button("Gerar Relatório Xperience")
        
        if submitted:
            # Validate inputs
            if not business_name:
                st.error("Por favor, informe o nome da empresa.")
                return False
            
            if not products_services:
                st.error("Por favor, informe os produtos/serviços atuais.")
                return False
            
            if not target_customers:
                st.error("Por favor, informe o cliente-alvo.")
                return False
            
            # Store data in session state
            st.session_state.form_data = {
                'business_name': business_name,
                'products_services': products_services,
                'competitors': competitors,
                'target_customers': target_customers,
                'differentials': differentials,
                'challenges': challenges,
                'goals': goals,
                'strengths': strengths,
                'limitations': limitations
            }
            
            return True
    
    return False

def render_seo_form():
    """Render form for SEO report"""
    st.subheader("Informe os dados para gerar seu Relatório SEO")
    
    with st.form("seo_form"):
        # Website information
        business_name = st.text_input("Nome da empresa", max_chars=100)
        website_url = st.text_input(
            "URL do site",
            placeholder="https://www.exemplo.com"
        )
        
        # Keywords
        keywords = st.text_area(
            "Palavras-chave target (separadas por vírgula)",
            placeholder="Ex: consultoria financeira, planejamento tributário, gestão de investimentos"
        )
        
        # Competitors
        competitors = st.text_area(
            "Sites concorrentes (separados por vírgula)",
            placeholder="Ex: www.concorrente1.com, www.concorrente2.com"
        )
        
        # Digital presence
        col1, col2 = st.columns(2)
        with col1:
            digital_channels = st.multiselect(
                "Canais digitais utilizados",
                options=[
                    "Site/Blog",
                    "Instagram",
                    "Facebook",
                    "LinkedIn",
                    "YouTube",
                    "Twitter",
                    "TikTok",
                    "Email Marketing",
                    "Google Ads",
                    "Facebook Ads"
                ]
            )
        
        with col2:
            site_age = st.selectbox(
                "Idade do site",
                options=[
                    "Menos de 6 meses",
                    "6 meses a 1 ano",
                    "1 a 3 anos",
                    "3 a 5 anos",
                    "Mais de 5 anos"
                ]
            )
        
        # Goals
        goals = st.text_area(
            "Objetivos da presença online",
            placeholder="Ex: Aumentar tráfego orgânico, Gerar mais leads, Melhorar conversões"
        )
        
        # Target audience
        target_audience = st.text_area(
            "Público-alvo online",
            placeholder="Ex: Profissionais de RH entre 30-45 anos em empresas de médio porte"
        )
        
        # Submit button
        submitted = st.form_submit_button("Gerar Relatório SEO")
        
        if submitted:
            # Validate inputs
            if not business_name:
                st.error("Por favor, informe o nome da empresa.")
                return False
            
            if not website_url:
                st.error("Por favor, informe a URL do site.")
                return False
            
            if not validate_url(website_url):
                st.error("Por favor, informe uma URL válida (ex: https://www.exemplo.com).")
                return False
            
            if not keywords:
                st.error("Por favor, informe as palavras-chave target.")
                return False
            
            # Store data in session state
            st.session_state.form_data = {
                'business_name': business_name,
                'website_url': website_url,
                'keywords': keywords,
                'competitors': competitors,
                'digital_channels': digital_channels,
                'site_age': site_age,
                'goals': goals,
                'target_audience': target_audience
            }
            
            return True
    
    return False
