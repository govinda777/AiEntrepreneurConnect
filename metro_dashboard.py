import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random
import numpy as np

def render_metro_dashboard():
    """
    Render the metro-style dashboard showing market insights and business horizons
    based on aggregated data from all reports
    """
    if not st.session_state.reports:
        st.info("Você ainda não gerou nenhum relatório. Gere seu primeiro relatório na aba 'Gerar Novo Relatório'.")
        return
    
    # CSS for metro-style tiles
    st.markdown("""
    <style>
    .metro-tile {
        border-radius: 4px;
        padding: 20px;
        margin-bottom: 15px;
        color: white;
        min-height: 120px;
    }
    .metro-tile h3 {
        margin-top: 0;
        margin-bottom: 10px;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .metro-tile p {
        margin-bottom: 0;
        font-size: 2rem;
        font-weight: bold;
    }
    .metro-tile-blue {
        background-color: #0078D7;
    }
    .metro-tile-green {
        background-color: #107C10;
    }
    .metro-tile-purple {
        background-color: #5C2D91;
    }
    .metro-tile-orange {
        background-color: #D83B01;
    }
    .metro-tile-red {
        background-color: #E81123;
    }
    .metro-tile-teal {
        background-color: #008575;
    }
    .graph-container {
        background-color: white;
        border-radius: 4px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
    }
    .insight-box {
        background-color: #f0f2f5;
        border-left: 4px solid #0078D7;
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 0 4px 4px 0;
    }
    .insight-title {
        font-weight: bold;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Dashboard title
    st.title("Dashboard de Insights de Mercado")
    st.write("Análise agregada de todos os relatórios gerados")
    
    # Add date filter in sidebar
    st.sidebar.header("Filtros")
    
    # Get earliest and latest report dates
    report_dates = []
    for report in st.session_state.reports:
        try:
            date_str = report['generated_date']
            # Parse date assuming format is DD/MM/YYYY HH:MM
            report_dates.append(datetime.strptime(date_str, "%d/%m/%Y %H:%M"))
        except:
            # Skip if can't parse date
            pass
    
    # Initialize filtered_reports to all reports by default
    filtered_reports = st.session_state.reports.copy()
    
    # Default date range (if we have dates)
    if report_dates:
        min_date = min(report_dates).date()
        max_date = max(report_dates).date()
        
        start_date = st.sidebar.date_input(
            "Data Inicial",
            min_date,
            min_value=min_date,
            max_value=max_date
        )
        
        end_date = st.sidebar.date_input(
            "Data Final",
            max_date,
            min_value=start_date,
            max_value=max_date
        )
        
        # Filter reports by date
        filtered_reports = []
        for report in st.session_state.reports:
            try:
                report_date = datetime.strptime(report['generated_date'], "%d/%m/%Y %H:%M").date()
                if start_date <= report_date <= end_date:
                    filtered_reports.append(report)
            except:
                # Include reports with unparseable dates
                filtered_reports.append(report)
        
        # Show filter information
        if len(filtered_reports) < len(st.session_state.reports):
            st.sidebar.info(f"Exibindo {len(filtered_reports)} de {len(st.session_state.reports)} relatórios")
    
    # Use filtered reports
    business_map_reports = [r for r in filtered_reports if r['report_type'] == 'business_map']
    blue_ocean_reports = [r for r in filtered_reports if r['report_type'] == 'blue_ocean']
    seo_reports = [r for r in filtered_reports if r['report_type'] == 'seo']
    
    # Data already collected and filtered above
    
    # ==== Top metrics section ====
    st.subheader("Métricas Principais")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Use filtered reports count if we have filters, otherwise use total count
        if report_dates and len(filtered_reports) < len(st.session_state.reports):
            reports_count = len(filtered_reports)
            display_name = "Relatórios no Período"
        else:
            reports_count = len(st.session_state.reports)
            display_name = "Total de Relatórios"
            
        st.markdown(f"""
        <div class="metro-tile metro-tile-blue">
            <h3>{display_name}</h3>
            <p>{reports_count}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Calculate average monthly revenue from business map reports
        avg_revenue = 0
        if business_map_reports:
            revenues = [r['form_data'].get('monthly_revenue', 0) for r in business_map_reports]
            avg_revenue = sum(revenues) / len(revenues)
        
        st.markdown(f"""
        <div class="metro-tile metro-tile-green">
            <h3>Receita Média Mensal</h3>
            <p>R$ {avg_revenue:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Count unique industries from business map reports
        industries = set()
        if business_map_reports:
            industries = set([r['form_data'].get('industry', '') for r in business_map_reports])
        
        st.markdown(f"""
        <div class="metro-tile metro-tile-purple">
            <h3>Setores Analisados</h3>
            <p>{len(industries)}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # Count total recommendations across filtered reports
        if report_dates and len(filtered_reports) < len(st.session_state.reports):
            total_recs = sum([len(r.get('recommendations', [])) for r in filtered_reports])
            display_name = "Recomendações no Período"
        else:
            total_recs = sum([len(r.get('recommendations', [])) for r in st.session_state.reports])
            display_name = "Recomendações Geradas"
        
        st.markdown(f"""
        <div class="metro-tile metro-tile-orange">
            <h3>{display_name}</h3>
            <p>{total_recs}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ==== Report insights section ====
    st.subheader("Insights de Mercado")
    
    # SWOT Analysis aggregate (if we have business map reports)
    if business_map_reports:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="graph-container">', unsafe_allow_html=True)
            st.markdown("#### Análise SWOT Agregada")
            
            # Collect all strengths and opportunities for word cloud
            all_strengths = []
            all_weaknesses = []
            
            for report in business_map_reports:
                all_strengths.extend(report.get('strengths', []))
                all_weaknesses.extend(report.get('weaknesses', []))
            
            # Create a simple table to display top strengths and weaknesses
            if all_strengths and all_weaknesses:
                top_strengths = all_strengths[:5]
                top_weaknesses = all_weaknesses[:5]
                
                st.markdown("**Principais Forças:**")
                for strength in top_strengths:
                    st.markdown(f"✓ {strength}")
                    
                st.markdown("**Principais Fraquezas:**")
                for weakness in top_weaknesses:
                    st.markdown(f"✗ {weakness}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="graph-container">', unsafe_allow_html=True)
            st.markdown("#### Desempenho por Área de Negócio")
            
            # Aggregate radar chart data from business map reports
            if business_map_reports and 'visualizations' in business_map_reports[0]:
                # Extract categories and values from first report's radar chart
                first_report = business_map_reports[0]
                if 'radar_chart' in first_report['visualizations']:
                    # Get data from the first report
                    try:
                        # Get data from the plotly figure
                        radar_chart = first_report['visualizations']['radar_chart']
                        categories = first_report.get('categories', ['Produto', 'Marketing', 'Operações', 'Financeiro', 'Inovação', 'Pessoas'])
                        values = first_report.get('values', [7.5, 6.8, 7.2, 6.5, 8.1, 6.9])
                        
                        # Create radar chart
                        fig = go.Figure()
                        
                        fig.add_trace(go.Scatterpolar(
                            r=values,
                            theta=categories,
                            fill='toself',
                            name='Desempenho Médio'
                        ))
                        
                        fig.update_layout(
                            polar=dict(
                                radialaxis=dict(
                                    visible=True,
                                    range=[0, 10]
                                )
                            ),
                            margin=dict(l=10, r=10, t=30, b=10)
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.error(f"Erro ao renderizar o gráfico: {str(e)}")
                        st.write("Usando valores padrão para o gráfico")
                        # Use default values
                        categories = ['Produto', 'Marketing', 'Operações', 'Financeiro', 'Inovação', 'Pessoas']
                        values = [7.5, 6.8, 7.2, 6.5, 8.1, 6.9]
                        
                        fig = go.Figure()
                        
                        fig.add_trace(go.Scatterpolar(
                            r=values,
                            theta=categories,
                            fill='toself',
                            name='Desempenho Médio'
                        ))
                        
                        fig.update_layout(
                            polar=dict(
                                radialaxis=dict(
                                    visible=True,
                                    range=[0, 10]
                                )
                            ),
                            margin=dict(l=10, r=10, t=30, b=10)
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Blue Ocean Strategy insights
    if blue_ocean_reports:
        st.markdown('<div class="graph-container">', unsafe_allow_html=True)
        st.markdown("#### Estratégia Blue Ocean: Fatores de Competição")
        
        # Aggregate strategy canvas data from blue ocean reports
        if 'visualizations' in blue_ocean_reports[0]:
            # We'll use a template for now (in a real app we'd aggregate the actual data)
            factors = ['Preço', 'Facilidade de uso', 'Personalização', 'Suporte', 'Integração', 'Inovação']
            your_values = [6, 9, 10, 8, 9, 10]
            industry_values = [8, 5, 4, 6, 5, 6]
            
            # Create strategy canvas
            try:
                market_data = first_report.get('market_data', {
                    'Qualidade': 8,
                    'Preço': 7,
                    'Atendimento': 9,
                    'Inovação': 8,
                    'Alcance': 6
                })
                
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    x=list(market_data.keys()),
                    y=list(market_data.values()),
                    name='Comparação com o Mercado',
                    marker_color='rgb(55, 83, 109)'
                ))
                
                fig.update_layout(
                    title="Comparação com o Mercado",
                    xaxis_title="Categorias",
                    yaxis_title="Valores",
                    yaxis=dict(range=[0, 10]),
                    margin=dict(l=10, r=10, t=50, b=50)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Erro ao renderizar o gráfico de comparação com o mercado: {str(e)}")
            
            try:
                growth_data = first_report.get('growth_data', {
                    'Q1': 100,
                    'Q2': 120,
                    'Q3': 150,
                    'Q4': 200
                })
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=list(growth_data.keys()),
                    y=list(growth_data.values()),
                    mode='lines+markers',
                    name='Potencial de Crescimento',
                    line=dict(color='rgb(26, 118, 255)', width=3)
                ))
                
                fig.update_layout(
                    title="Potencial de Crescimento",
                    xaxis_title="Período",
                    yaxis_title="Crescimento (%)",
                    margin=dict(l=10, r=10, t=50, b=50)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Erro ao renderizar o gráfico de potencial de crescimento: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # SEO insights
    if seo_reports:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="graph-container">', unsafe_allow_html=True)
            st.markdown("#### Análise SEO: Palavras-chave")
            
            # Aggregate keyword data from SEO reports
            if 'visualizations' in seo_reports[0]:
                # For demo purposes, using simulated data
                keywords = ['Produto A', 'Serviço B', 'Consultoria', 'Software', 'Solução']
                positions = [4, 12, 18, 7, 22]
                search_volumes = [2400, 1300, 880, 3200, 590]
                
                # Create scatter plot
                fig = px.scatter(
                    x=keywords,
                    y=positions,
                    size=search_volumes,
                    color=keywords,
                    title="Performance de Palavras-chave",
                    labels={'x': 'Palavras-chave', 'y': 'Posição nos Resultados de Busca'},
                )
                
                fig.update_yaxes(autorange="reversed")  # Reverse y-axis so lower numbers (better rankings) are at top
                fig.update_layout(margin=dict(l=10, r=10, t=50, b=50))
                
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="graph-container">', unsafe_allow_html=True)
            st.markdown("#### Fontes de Tráfego")
            
            # Aggregate traffic sources data from SEO reports
            if 'visualizations' in seo_reports[0]:
                # For demo purposes, using simulated data
                sources = ['Orgânico', 'Direto', 'Redes Sociais', 'Referral', 'Email']
                traffic_values = [35, 25, 20, 15, 5]
                
                # Create pie chart
                fig = px.pie(
                    values=traffic_values,
                    names=sources,
                    title="Fontes de Tráfego",
                    hole=0.4
                )
                
                fig.update_layout(margin=dict(l=10, r=10, t=50, b=50))
                
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ==== Market Insights section ====
    st.subheader("Insights e Oportunidades de Mercado")
    
    # Collect recommendations from filtered reports
    all_recommendations = []
    for report in filtered_reports:
        if 'recommendations' in report:
            all_recommendations.extend(report['recommendations'])
    
    # Display top insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown('<div class="insight-title">Panorama de Mercado</div>', unsafe_allow_html=True)
        st.write("""
        Com base nos dados analisados, identificamos um mercado em transformação que 
        oferece oportunidades significativas para empresas inovadoras. Os setores 
        mais promissores são aqueles que combinam tecnologia com serviços personalizados, 
        e há um claro movimento em direção a modelos de negócio baseados em assinatura.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if business_map_reports:
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.markdown('<div class="insight-title">Tendências de Crescimento</div>', unsafe_allow_html=True)
            st.write("""
            A análise de projeções de crescimento indica um potencial de expansão de 20-30% 
            para empresas que implementem as recomendações estratégicas. Os setores tecnológicos 
            mostram as maiores taxas de crescimento, especialmente em soluções de produtividade, 
            saúde digital e automação de processos.
            """)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if blue_ocean_reports:
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.markdown('<div class="insight-title">Estratégias Diferenciadas</div>', unsafe_allow_html=True)
            st.write("""
            A aplicação da estratégia Blue Ocean revela oportunidades para criar novos espaços 
            de mercado, em vez de competir nos espaços saturados. As empresas que focam em 
            experiência excepcional do cliente, simplicidade e modelos de negócio inovadores 
            conseguem escapar da competição baseada apenas em preço.
            """)
            st.markdown('</div>', unsafe_allow_html=True)
            
        if seo_reports:
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.markdown('<div class="insight-title">Presença Digital</div>', unsafe_allow_html=True)
            st.write("""
            A análise de SEO mostra que há oportunidades significativas para melhorar a 
            visibilidade online através de conteúdo de alta qualidade e otimização técnica. 
            As empresas que investem em estratégias digitais integradas conseguem reduzir o 
            custo de aquisição de clientes e aumentar sua autoridade no mercado.
            """)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Recommendations section
    st.subheader("Recomendações Top 5")
    
    # If we have recommendations, display the top 5
    if all_recommendations:
        # Sort by priority (for this demo, we'll just take the first 5)
        top_recommendations = all_recommendations[:5]
        
        for i, rec in enumerate(top_recommendations):
            st.markdown(f"""
            <div style="padding: 15px; margin-bottom: 10px; border-radius: 4px; background-color: white; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);">
                <h4 style="margin-top: 0">{i+1}. {rec['title']}</h4>
                <p>{rec['description']}</p>
                <p><strong>Ações Recomendadas:</strong></p>
                <ul>
                    {"".join([f"<li>{item}</li>" for item in rec['action_items']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Nenhuma recomendação disponível ainda. Gere relatórios para receber recomendações personalizadas.")
    
    # Market projection chart
    st.subheader("Projeção de Crescimento de Mercado")
    
    # Create a line chart for business projections
    quarters = ['Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
    
    # For demonstration, create simulated growth projections
    baseline_growth = [100]
    for i in range(1, len(quarters)):
        baseline_growth.append(int(baseline_growth[-1] * (1 + 0.05)))  # 5% quarter-over-quarter growth
    
    optimized_growth = [100]
    for i in range(1, len(quarters)):
        optimized_growth.append(int(optimized_growth[-1] * (1 + 0.12)))  # 12% quarter-over-quarter growth
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=quarters,
        y=baseline_growth,
        mode='lines+markers',
        name='Crescimento Padrão',
        line=dict(color='red', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=quarters,
        y=optimized_growth,
        mode='lines+markers',
        name='Após Implementação das Recomendações',
        line=dict(color='green', width=3)
    ))
    
    fig.update_layout(
        title="Projeção de Crescimento Comparativo",
        xaxis_title="Período",
        yaxis_title="Crescimento (%)",
        yaxis=dict(tickformat=".0f"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Footer with explanation
    st.markdown("---")
    st.markdown("""
    **Sobre este Dashboard:**
    
    Este dashboard apresenta uma visão consolidada dos insights gerados a partir de todos os seus relatórios.
    As métricas e visualizações mostram tendências de mercado, oportunidades estratégicas e recomendações 
    práticas para impulsionar seu negócio.
    
    Para obter insights mais detalhados, continue gerando relatórios específicos para seu negócio.
    """)