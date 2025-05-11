import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import uuid
import datetime
import random
from utils import (
    generate_radar_chart, 
    generate_bar_chart, 
    generate_line_chart
)
from api_client import AIClient

def generate_report(report_type, form_data):
    """
    Generate a report based on the report type and form data
    
    This uses OpenAI's API via the AIClient to generate intelligent insights
    based on the user's input data.
    """
    
    # Create report ID and timestamp
    report_id = str(uuid.uuid4())
    generated_date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # Map report types to display names
    report_type_display = {
        "business_map": "Mapa do Seu Negócio",
        "blue_ocean": "Relatório Xperience (Blue Ocean)",
        "seo": "Relatório SEO"
    }.get(report_type, "Relatório Personalizado")
    
    # Pre-process form data to ensure all required fields are present
    form_data = {k: v for k, v in form_data.items() if v is not None and v != ""}
    
    # Initialize AI client
    ai_client = AIClient()
    
    try:
        # Generate AI analysis based on report type
        if report_type == "business_map":
            ai_analysis = ai_client.analyze_business(form_data)
        elif report_type == "blue_ocean":
            ai_analysis = ai_client.generate_blue_ocean_strategy(form_data)
        elif report_type == "seo":
            ai_analysis = ai_client.analyze_seo(form_data)
        else:
            raise ValueError(f"Tipo de relatório inválido: {report_type}")
        
        # Create base report structure
        report = {
            "id": report_id,
            "generated_date": generated_date,
            "report_type": report_type,
            "report_type_display": report_type_display,
            "form_data": form_data,
            "ai_analysis": ai_analysis
        }
        
        # Add report-specific data and visualizations
        if report_type == "business_map":
            report.update(_generate_business_map_report(form_data, ai_analysis))
        elif report_type == "blue_ocean":
            report.update(_generate_blue_ocean_report(form_data, ai_analysis))
        elif report_type == "seo":
            report.update(_generate_seo_report(form_data, ai_analysis))
        
        return report
        
    except Exception as e:
        st.error(f"Erro ao gerar relatório: {str(e)}")
        raise

def _generate_business_map_report(form_data, ai_analysis):
    """Generate business map specific report content"""
    business_name = form_data.get('business_name', 'Empresa')
    
    return {
        "title": f"Mapa Estratégico: {business_name}",
        "executive_summary": (
            f"Este relatório apresenta uma análise detalhada da situação atual de {business_name}, "
            "identificando oportunidades de crescimento e áreas para otimização."
        ),
        "visualizations": {
            "radar_chart": generate_radar_chart(
                ai_analysis.get('categories', []),
                ai_analysis.get('values', []),
                "Desempenho por Área"
            ),
            "market_comparison": generate_bar_chart(
                ai_analysis.get('market_data', {}),
                "Comparação com o Mercado"
            ),
            "growth_potential": generate_line_chart(
                ai_analysis.get('growth_data', {}),
                "Potencial de Crescimento"
            )
        }
    }

def _generate_blue_ocean_report(form_data, ai_analysis):
    """Generate Blue Ocean specific report content"""
    business_name = form_data.get('business_name', 'Empresa')
    
    return {
        "title": f"Estratégia Blue Ocean: {business_name}",
        "executive_summary": (
            f"Este relatório apresenta uma análise Blue Ocean para {business_name}, "
            "identificando oportunidades de criação de novo espaço de mercado."
        ),
        "visualizations": {
            "strategy_canvas": _create_strategy_canvas(ai_analysis),
            "actions_chart": _create_actions_chart(ai_analysis),
            "performance_projection": _create_performance_projection(ai_analysis)
        }
    }

def _generate_seo_report(form_data, ai_analysis):
    """Generate SEO specific report content"""
    business_name = form_data.get('business_name', 'Empresa')
    website_url = form_data.get('website_url', 'exemplo.com')
    
    return {
        "title": f"Análise SEO: {business_name}",
        "executive_summary": (
            f"Este relatório apresenta uma análise detalhada da presença online de {business_name} "
            f"({website_url}), com recomendações para otimização."
        ),
        "visualizations": {
            "keyword_performance": _create_keyword_chart(ai_analysis),
            "traffic_sources": _create_traffic_chart(ai_analysis),
            "optimization_opportunities": _create_optimization_chart(ai_analysis)
        }
    }

def _create_strategy_canvas(ai_analysis):
    """Create strategy canvas visualization"""
    factors = ai_analysis.get('canvas_factors', [])
    your_values = ai_analysis.get('your_values', [])
    industry_values = ai_analysis.get('industry_values', [])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=factors,
        y=your_values,
        name='Sua Empresa',
        line=dict(color='blue', width=4)
    ))
    
    fig.add_trace(go.Scatter(
        x=factors,
        y=industry_values,
        name='Concorrentes',
        line=dict(color='red', width=4)
    ))
    
    fig.update_layout(
        title="Canvas Estratégico: Sua Empresa vs. Concorrentes",
        xaxis_title="Fatores de Competição",
        yaxis_title="Nível de Oferta",
        yaxis=dict(range=[0, 10])
    )
    
    return fig

def _create_actions_chart(ai_analysis):
    """Create actions chart visualization"""
    actions = ["Eliminar", "Reduzir", "Aumentar", "Criar"]
    action_counts = [
        len(ai_analysis.get('eliminate', [])),
        len(ai_analysis.get('reduce', [])),
        len(ai_analysis.get('raise', [])),
        len(ai_analysis.get('create', []))
    ]
    
    return px.bar(
        x=actions,
        y=action_counts,
        color=actions,
        title="Framework ERRC (Eliminar-Reduzir-Aumentar-Criar)",
        labels={'x': 'Ações Estratégicas', 'y': 'Quantidade de Elementos'}
    )

def _create_performance_projection(ai_analysis):
    """Create performance projection visualization"""
    years = [f"Ano {i}" for i in range(1, 6)]
    blue_ocean = [100, 150, 225, 340, 510]  # 50% growth YoY
    red_ocean = [100, 110, 121, 133, 146]   # 10% growth YoY
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=years,
        y=blue_ocean,
        name='Estratégia Blue Ocean',
        line=dict(color='blue', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=years,
        y=red_ocean,
        name='Mercado Tradicional',
        line=dict(color='red', width=3)
    ))
    
    fig.update_layout(
        title="Projeção de Performance (5 anos)",
        xaxis_title="Período",
        yaxis_title="Crescimento (%)"
    )
    
    return fig

def _create_keyword_chart(ai_analysis):
    """Create keyword performance visualization"""
    keywords_data = ai_analysis.get('keywords_data', {})
    
    return px.scatter(
        x=keywords_data.get('keywords', []),
        y=keywords_data.get('positions', []),
        size=keywords_data.get('search_volumes', []),
        title="Performance de Palavras-chave",
        labels={'x': 'Palavras-chave', 'y': 'Posição nos Resultados de Busca'}
    )

def _create_traffic_chart(ai_analysis):
    """Create traffic sources visualization"""
    traffic_data = ai_analysis.get('traffic_sources', {})
    
    return px.pie(
        values=traffic_data.get('percentages', []),
        names=traffic_data.get('sources', []),
        title="Fontes de Tráfego",
        hole=0.4
    )

def _create_optimization_chart(ai_analysis):
    """Create optimization opportunities visualization"""
    opportunities = ai_analysis.get('optimization_opportunities', [])
    
    areas = [opp['area'] for opp in opportunities]
    impact = [opp['impact'] for opp in opportunities]
    difficulty = [opp['difficulty'] for opp in opportunities]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Impacto',
        x=areas,
        y=impact,
        marker_color='blue'
    ))
    
    fig.add_trace(go.Bar(
        name='Dificuldade',
        x=areas,
        y=difficulty,
        marker_color='red'
    ))
    
    fig.update_layout(
        barmode='group',
        title="Oportunidades de Otimização",
        xaxis_title="Áreas",
        yaxis_title="Pontuação"
    )
    
    return fig

def generate_sample_reports():
    """Generate sample reports for testing"""
    
    # Only generate if no reports exist yet
    if 'reports' not in st.session_state or not st.session_state.reports:
        st.session_state.reports = []
        
        # Sample Business Map report
        business_map_data = {
            'business_name': 'Tech Solutions',
            'industry': 'Tecnologia',
            'business_model': 'SaaS',
            'monthly_revenue': 120000,
            'employees': 15,
            'main_products': 'Software de Gestão, Consultoria',
            'target_audience': 'Pequenas e Médias Empresas'
        }
        
        business_map_report = generate_report('business_map', business_map_data)
        if business_map_report:
            st.session_state.reports.append(business_map_report)
        
        # Sample Blue Ocean report
        blue_ocean_data = {
            'business_name': 'Inova Marketing',
            'products_services': 'Marketing Digital, Branding',
            'competitors': 'AgênciaX, MarketingPro',
            'target_customers': 'Startups e Empresas de Tecnologia',
            'differentials': 'Marketing Baseado em Dados, Estratégias Personalizadas',
            'goals': 'Expandir para novos mercados, Aumentar ticket médio'
        }
        
        blue_ocean_report = generate_report('blue_ocean', blue_ocean_data)
        if blue_ocean_report:
            st.session_state.reports.append(blue_ocean_report)
        
        # Sample SEO report
        seo_data = {
            'business_name': 'Ecommerce Shop',
            'website_url': 'https://www.ecommerceshop.com',
            'keywords': 'ecommerce, loja online, produtos sustentáveis',
            'competitors': 'competitor1.com, competitor2.com',
            'goals': 'Aumentar tráfego orgânico, Melhorar taxa de conversão',
            'channels': 'Google, Redes Sociais, Blog'
        }
        
        seo_report = generate_report('seo', seo_data)
        if seo_report:
            st.session_state.reports.append(seo_report)
