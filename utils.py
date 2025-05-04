import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
from io import BytesIO
import random
import datetime
import json
import re

# Templates for AI prompts
BLUE_OCEAN_TEMPLATE = """
# 🌊 Estratégia Blue Ocean para {business_name}

A Estratégia Blue Ocean, desenvolvida por W. Chan Kim e Renée Mauborgne, propõe que as empresas criem novos espaços de mercado inexplorados ("oceanos azuis") em vez de competir em mercados saturados ("oceanos vermelhos"). Este estudo de caso apresenta como a {business_name} pode implementar esta abordagem revolucionária no setor de {industry}.

## 📊 Strategy Canvas (Tela Estratégica)

A Tela Estratégica é o principal instrumento visual da Estratégia Blue Ocean, permitindo comparar a oferta da {business_name} com a dos concorrentes tradicionais em diversos fatores competitivos.

## 🔄 Framework das Quatro Ações

O Framework das Quatro Ações é essencial para criar uma nova curva de valor para a {business_name}:

1. **Eliminar** ✂️
   - [Lista de elementos a eliminar]

2. **Reduzir** ⬇️
   - [Lista de elementos a reduzir]

3. **Aumentar** ⬆️
   - [Lista de elementos a aumentar]

4. **Criar** 🆕
   - [Lista de elementos a criar]

## 📈 Comparação de Performance Projetada

O gráfico abaixo demonstra a projeção de crescimento da {business_name} comparada com empresas tradicionais do setor.

## 🔍 Três Características da Estratégia Blue Ocean da {business_name}

A estratégia da {business_name} apresenta as três qualidades essenciais de uma boa estratégia Blue Ocean:

1. **Foco**: [Descrição de foco]
2. **Divergência**: [Descrição de divergência]
3. **Mensagem Clara**: [Mensagem clara]

## Recomendações Estratégicas

1. [Recomendação 1 com descrição e ações]
2. [Recomendação 2 com descrição e ações]
3. [Recomendação 3 com descrição e ações]

## 📚 Conclusão

[Conclusão do relatório]
"""

BUSINESS_MAP_TEMPLATE = """
# 🗺️ Mapa Estratégico para {business_name}

## Resumo Executivo
[Resumo executivo da empresa e do setor]

## Análise SWOT

### Forças
- [Lista de forças]

### Fraquezas
- [Lista de fraquezas]

### Oportunidades
- [Lista de oportunidades]

### Ameaças
- [Lista de ameaças]

## Análise de Mercado
[Análise detalhada do mercado e posicionamento]

## Recomendações Estratégicas

1. [Recomendação 1 com descrição e ações]
2. [Recomendação 2 com descrição e ações]
3. [Recomendação 3 com descrição e ações]

## Projeção de Crescimento
[Projeção de crescimento para os próximos períodos]

## Conclusão
[Conclusão do relatório com próximos passos recomendados]
"""

SEO_REPORT_TEMPLATE = """
# 🔍 Análise SEO para {business_name}

## Resumo Executivo
[Resumo da análise e principais achados]

## Pontuação SEO Geral: [score]/100

## Análise de Palavras-chave
[Análise detalhada das palavras-chave principais]

## Fontes de Tráfego
[Análise das principais fontes de tráfego]

## Oportunidades de Otimização

1. **[Área 1]**
   - Impacto: [valor]/100
   - Dificuldade: [valor]/100
   - [Recomendações específicas]

2. **[Área 2]**
   - Impacto: [valor]/100
   - Dificuldade: [valor]/100
   - [Recomendações específicas]

3. **[Área 3]**
   - Impacto: [valor]/100
   - Dificuldade: [valor]/100
   - [Recomendações específicas]

## Recomendações Estratégicas

1. [Recomendação 1 com descrição e ações]
2. [Recomendação 2 com descrição e ações]
3. [Recomendação 3 com descrição e ações]

## Conclusão
[Conclusão da análise com projeção de resultados após implementação]
"""

def set_page_config():
    """Configure the page settings for the Streamlit app"""
    st.set_page_config(
        page_title="IA do Empreendedor",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

def load_css():
    """Load custom CSS for the app"""
    # This function is here for future customization if needed
    # As per guidelines, we're using Streamlit's default styling
    pass

def format_wallet_address(address):
    """Format wallet address for display by truncating the middle part"""
    if address and len(address) > 10:
        return f"{address[:6]}...{address[-4:]}"
    return address

def create_download_link(df, filename="data.csv"):
    """Create a download link for a DataFrame"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV</a>'
    return href

def create_pdf_download_link(content, filename="report.pdf"):
    """Create a download link for a PDF (simulated for this demo)"""
    # Note: This is a placeholder function. In a real implementation,
    # you'd generate an actual PDF file using a library like ReportLab or PyPDF2
    href = f'<a href="#" download="{filename}">Download PDF</a>'
    return href

def generate_radar_chart(categories, values, title):
    """Generate a radar chart using Plotly"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Your Business'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        title=title,
        showlegend=True
    )
    
    return fig

def generate_bar_chart(x_data, y_data, title, x_label, y_label):
    """Generate a bar chart using Plotly"""
    fig = px.bar(
        x=x_data, 
        y=y_data, 
        title=title,
        labels={'x': x_label, 'y': y_label}
    )
    return fig

def generate_line_chart(x_data, y_data, title, x_label, y_label):
    """Generate a line chart using Plotly"""
    fig = px.line(
        x=x_data, 
        y=y_data, 
        title=title,
        labels={'x': x_label, 'y': y_label}
    )
    return fig

def validate_url(url):
    """Validate if a string is a properly formatted URL"""
    url_pattern = re.compile(
        r'^(?:http|https)://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return bool(url_pattern.match(url))

def display_report(report):
    """Display a generated report in the Streamlit interface"""
    st.title(report['title'])
    
    # Display report metadata
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Data de geração:** {report['generated_date']}")
        st.write(f"**Tipo de relatório:** {report['report_type_display']}")
    with col2:
        st.write(f"**ID do relatório:** {report['id']}")
        
    # Display executive summary
    st.header("Resumo Executivo")
    st.write(report['executive_summary'])
    
    # Display visualizations
    st.header("Análise de Dados")
    
    # Handle different report types
    if report['report_type'] == 'business_map':
        # Business Map specific visualizations
        st.subheader("Mapa de Desempenho por Área")
        st.plotly_chart(report['visualizations']['radar_chart'], use_container_width=True)
        
        st.subheader("Comparação com o Mercado")
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(report['visualizations']['market_comparison'], use_container_width=True)
        with col2:
            st.plotly_chart(report['visualizations']['growth_potential'], use_container_width=True)
            
    elif report['report_type'] == 'blue_ocean':
        # Blue Ocean specific visualizations
        st.subheader("Estratégia Canvas")
        st.plotly_chart(report['visualizations']['strategy_canvas'], use_container_width=True)
        
        st.subheader("Ações Estratégicas")
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(report['visualizations']['actions_chart'], use_container_width=True) 
        with col2:
            st.plotly_chart(report['visualizations']['performance_projection'], use_container_width=True)
            
    elif report['report_type'] == 'seo':
        # SEO specific visualizations
        st.subheader("Performance de Palavras-chave")
        st.plotly_chart(report['visualizations']['keyword_performance'], use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Tráfego por Canal")
            st.plotly_chart(report['visualizations']['traffic_sources'], use_container_width=True)
        with col2:
            st.subheader("Oportunidades de Otimização")
            st.plotly_chart(report['visualizations']['optimization_opportunities'], use_container_width=True)
    
    # Display recommendations
    st.header("Recomendações Estratégicas")
    for i, recommendation in enumerate(report['recommendations'], 1):
        st.subheader(f"{i}. {recommendation['title']}")
        st.write(recommendation['description'])
        
        # Show action items if any
        if 'action_items' in recommendation and recommendation['action_items']:
            st.write("**Ações recomendadas:**")
            for action in recommendation['action_items']:
                st.write(f"- {action}")
    
    # Display conclusion
    st.header("Conclusão")
    st.write(report['conclusion'])
    
    # Download options
    st.header("Download do Relatório")
    col1, col2 = st.columns(2)
    with col1:
        # PDF download (simulated)
        pdf_link = create_pdf_download_link(report, f"{report['id']}.pdf")
        st.markdown(pdf_link, unsafe_allow_html=True)
    with col2:
        # CSV download of data (if applicable)
        if 'data' in report:
            csv_link = create_download_link(report['data'], f"{report['id']}.csv")
            st.markdown(csv_link, unsafe_allow_html=True)

def format_currency(value):
    """Format a value as BRL currency"""
    return f"R$ {value:,.2f}"
