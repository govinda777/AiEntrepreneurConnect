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

def generate_report(report_type, form_data):
    """
    Generate a report based on the report type and form data
    
    In a real implementation, this would call an AI service to analyze the data
    and generate insights. For this demo, we'll simulate the report generation.
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
    
    # Generate the appropriate report based on type
    if report_type == "business_map":
        report = generate_business_map_report(report_id, generated_date, form_data)
    elif report_type == "blue_ocean":
        report = generate_blue_ocean_report(report_id, generated_date, form_data)
    elif report_type == "seo":
        report = generate_seo_report(report_id, generated_date, form_data)
    else:
        st.error(f"Tipo de relatório desconhecido: {report_type}")
        return None
    
    # Return the complete report
    return report

def generate_business_map_report(report_id, generated_date, form_data):
    """Generate a Business Map report"""
    
    # Extract form data
    business_name = form_data.get('business_name', 'Empresa')
    industry = form_data.get('industry', 'Tecnologia')
    business_model = form_data.get('business_model', 'SaaS')
    monthly_revenue = form_data.get('monthly_revenue', 50000)
    employees = form_data.get('employees', 10)
    
    # Create report structure
    report = {
        "id": report_id,
        "generated_date": generated_date,
        "report_type": "business_map",
        "report_type_display": "Mapa do Seu Negócio",
        "title": f"Mapa Estratégico: {business_name}",
        "executive_summary": (
            f"{business_name} atua no setor de {industry} com um modelo de negócio {business_model}. "
            f"Com um faturamento mensal de R$ {monthly_revenue:,.2f} e {employees} colaboradores, "
            f"a empresa demonstra potencial para crescimento em áreas específicas, conforme detalhado neste relatório. "
            f"Análises de mercado e operacionais revelam oportunidades para otimização e expansão estratégica."
        ),
        "visualizations": {},
        "recommendations": [
            {
                "title": "Otimização de Processos Internos",
                "description": (
                    f"Baseado na análise do seu modelo de negócio {business_model}, identificamos oportunidades "
                    f"para melhorar a eficiência operacional através da automação de processos repetitivos e "
                    f"da implementação de metodologias ágeis."
                ),
                "action_items": [
                    "Implementar um sistema de gestão de processos",
                    "Treinar a equipe em metodologias ágeis",
                    "Automatizar relatórios e análises de desempenho"
                ]
            },
            {
                "title": "Expansão de Portfolio",
                "description": (
                    f"Para empresas do setor de {industry}, existe uma tendência de crescimento em soluções complementares. "
                    f"Recomendamos explorar novos produtos/serviços que se integrem ao seu atual portfólio."
                ),
                "action_items": [
                    "Realizar pesquisa de mercado para identificar necessidades não atendidas",
                    "Desenvolver um MVP (Minimum Viable Product) para testar novas ideias",
                    "Estabelecer parcerias estratégicas para expandir alcance"
                ]
            },
            {
                "title": "Estratégia de Crescimento Sustentável",
                "description": (
                    f"Considerando seu faturamento atual de R$ {monthly_revenue:,.2f} e estrutura de {employees} colaboradores, "
                    f"recomendamos uma estratégia de crescimento escalonável que mantenha a qualidade enquanto expande operações."
                ),
                "action_items": [
                    "Desenvolver um plano de contratações estratégicas",
                    "Implementar indicadores de desempenho (KPIs) alinhados aos objetivos de crescimento",
                    "Revisar a estrutura de custos para identificar eficiências"
                ]
            }
        ],
        "conclusion": (
            f"O mapeamento estratégico de {business_name} revela uma empresa com fundamentos sólidos e potencial significativo "
            f"para crescimento no setor de {industry}. A implementação das recomendações propostas pode resultar em um aumento "
            f"estimado de 20-30% em eficiência operacional e oportunidades de expansão de receita em novos mercados. "
            f"Recomendamos revisitar este mapa estratégico a cada trimestre para ajustes baseados nos resultados obtidos."
        ),
        "form_data": form_data
    }
    
    # Generate visualizations
    # 1. Radar chart for business areas performance
    categories = ['Produto', 'Marketing', 'Operações', 'Financeiro', 'Inovação', 'Pessoas']
    values = [random.uniform(5, 9) for _ in range(len(categories))]
    radar_chart = generate_radar_chart(
        categories=categories,
        values=values,
        title="Desempenho por Área"
    )
    
    # 2. Bar chart for market comparison
    competitors = ['Sua Empresa', 'Concorrente A', 'Concorrente B', 'Concorrente C']
    market_share = [
        random.uniform(15, 25),
        random.uniform(20, 30),
        random.uniform(15, 25),
        random.uniform(10, 20)
    ]
    market_comparison = generate_bar_chart(
        x_data=competitors,
        y_data=market_share,
        title="Participação de Mercado (%)",
        x_label="Empresas",
        y_label="Participação (%)"
    )
    
    # 3. Line chart for growth potential
    months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
    projected_growth = [monthly_revenue * (1 + random.uniform(0.03, 0.08) * i) for i in range(1, len(months) + 1)]
    growth_potential = generate_line_chart(
        x_data=months,
        y_data=projected_growth,
        title="Projeção de Crescimento (6 meses)",
        x_label="Mês",
        y_label="Receita Projetada (R$)"
    )
    
    # Add visualizations to report
    report['visualizations'] = {
        'radar_chart': radar_chart,
        'market_comparison': market_comparison,
        'growth_potential': growth_potential
    }
    
    return report

def generate_blue_ocean_report(report_id, generated_date, form_data):
    """Generate a Blue Ocean Strategy report"""
    
    # Extract form data
    business_name = form_data.get('business_name', 'Empresa')
    products_services = form_data.get('products_services', 'Software de Gestão')
    competitors = form_data.get('competitors', 'Empresa A, Empresa B')
    target_customers = form_data.get('target_customers', 'Pequenas e Médias Empresas')
    differentials = form_data.get('differentials', 'Facilidade de uso, Suporte personalizado')
    
    # Create report structure
    report = {
        "id": report_id,
        "generated_date": generated_date,
        "report_type": "blue_ocean",
        "report_type_display": "Relatório Xperience (Blue Ocean)",
        "title": f"Estratégia Blue Ocean: {business_name}",
        "executive_summary": (
            f"Este relatório apresenta uma análise Blue Ocean para {business_name}, que atua no mercado de {products_services}. "
            f"Identificamos oportunidades de criação de um novo espaço de mercado onde {business_name} pode se diferenciar "
            f"significativamente dos concorrentes ({competitors}), atendendo {target_customers} com uma proposta de valor única. "
            f"Seus diferenciais atuais ({differentials}) formam uma base sólida para esta estratégia."
        ),
        "visualizations": {},
        "recommendations": [
            {
                "title": "Eliminar fatores de competição tradicional",
                "description": (
                    f"Para criar um oceano azul, recomendamos eliminar elementos que o setor toma como certos mas que não "
                    f"agregam valor real para {target_customers}. Isso inclui processos complexos, funcionalidades raramente "
                    f"utilizadas e intermediários na cadeia de valor."
                ),
                "action_items": [
                    "Mapear e eliminar recursos pouco utilizados no produto",
                    "Simplificar o processo de onboarding de novos clientes",
                    "Reduzir dependência de canais tradicionais de distribuição"
                ]
            },
            {
                "title": "Criar novos fatores de valor",
                "description": (
                    f"Identificamos oportunidades para {business_name} criar elementos inovadores nunca oferecidos no setor. "
                    f"Isso inclui experiências personalizadas, modelos de precificação disruptivos e novas formas de interação "
                    f"com o produto."
                ),
                "action_items": [
                    "Desenvolver sistema de personalização baseado em IA",
                    "Introduzir modelo de precificação baseado em resultados",
                    "Criar plataforma de co-criação com clientes"
                ]
            },
            {
                "title": "Redefinir a experiência do cliente",
                "description": (
                    f"Com base nos diferencias atuais ({differentials}), recomendamos redefinir completamente a experiência "
                    f"do cliente, focando nos momentos-chave da jornada onde é possível criar valor excepcional."
                ),
                "action_items": [
                    "Mapear a jornada completa do cliente identificando pontos de frustração",
                    "Reimaginar o processo de suporte e sucesso do cliente",
                    "Implementar sistema de feedback contínuo e adaptação rápida"
                ]
            }
        ],
        "conclusion": (
            f"A estratégia Blue Ocean para {business_name} representa uma oportunidade de transformação do negócio, "
            f"posicionando-o em um espaço de mercado inexplorado onde a competição se torna irrelevante. "
            f"Implementando as recomendações deste relatório, estimamos um potencial de crescimento de 40-60% nos próximos "
            f"24 meses, com margens significativamente superiores à média do setor. O sucesso dependerá da execução "
            f"consistente desta estratégia e da capacidade de manter a inovação de valor como princípio central."
        ),
        "form_data": form_data
    }
    
    # Generate visualizations
    # 1. Strategy Canvas
    factors = ["Preço", "Variedade", "Atendimento", "Experiência", "Personalização", "Inovação"]
    your_values = [random.uniform(4, 8) for _ in range(len(factors))]
    competitors_values = [random.uniform(2, 9) for _ in range(len(factors))]
    
    strategy_canvas = go.Figure()
    
    strategy_canvas.add_trace(go.Scatter(
        x=factors,
        y=your_values,
        name='Sua Empresa (Futuro)',
        line=dict(color='blue', width=4)
    ))
    
    strategy_canvas.add_trace(go.Scatter(
        x=factors,
        y=competitors_values,
        name='Concorrentes (Atual)',
        line=dict(color='red', width=4)
    ))
    
    strategy_canvas.update_layout(
        title="Strategy Canvas: Sua Empresa vs. Concorrentes",
        xaxis_title="Fatores de Competição",
        yaxis_title="Nível de Oferta",
        yaxis=dict(range=[0, 10])
    )
    
    # 2. Actions Chart (ERRC Framework)
    actions = ["Eliminar", "Reduzir", "Aumentar", "Criar"]
    action_counts = [3, 2, 4, 3]
    
    actions_chart = px.bar(
        x=actions,
        y=action_counts,
        color=actions,
        title="Framework ERRC (Eliminar-Reduzir-Aumentar-Criar)",
        labels={'x': 'Ações Estratégicas', 'y': 'Quantidade de Elementos'}
    )
    
    # 3. Performance Projection
    years = [f"Ano {i}" for i in range(1, 6)]
    blue_ocean = [100, 150, 225, 340, 510]  # 50% growth YoY
    red_ocean = [100, 110, 121, 133, 146]   # 10% growth YoY
    
    performance_projection = go.Figure()
    
    performance_projection.add_trace(go.Scatter(
        x=years,
        y=blue_ocean,
        name='Estratégia Blue Ocean',
        line=dict(color='blue', width=3)
    ))
    
    performance_projection.add_trace(go.Scatter(
        x=years,
        y=red_ocean,
        name='Mercado Tradicional',
        line=dict(color='red', width=3)
    ))
    
    performance_projection.update_layout(
        title="Projeção de Performance (5 anos)",
        xaxis_title="Período",
        yaxis_title="Crescimento (%)",
    )
    
    # Add visualizations to report
    report['visualizations'] = {
        'strategy_canvas': strategy_canvas,
        'actions_chart': actions_chart,
        'performance_projection': performance_projection
    }
    
    return report

def generate_seo_report(report_id, generated_date, form_data):
    """Generate a SEO report"""
    
    # Extract form data
    website_url = form_data.get('website_url', 'https://example.com')
    business_name = form_data.get('business_name', 'Empresa')
    keywords = form_data.get('keywords', 'software, gestão, empresas')
    competitors = form_data.get('competitors', 'competitor1.com, competitor2.com')
    goals = form_data.get('goals', 'Aumentar tráfego orgânico e conversões')
    
    # Create report structure
    report = {
        "id": report_id,
        "generated_date": generated_date,
        "report_type": "seo",
        "report_type_display": "Relatório SEO",
        "title": f"Análise SEO: {business_name}",
        "executive_summary": (
            f"Este relatório apresenta uma análise completa da presença online de {business_name} ({website_url}). "
            f"Avaliamos o posicionamento para as palavras-chave target ({keywords}), comparamos com concorrentes "
            f"({competitors}) e identificamos oportunidades para atingir seus objetivos: {goals}. "
            f"Nossa análise revelou pontos fortes que podem ser potencializados e áreas críticas que exigem atenção imediata."
        ),
        "visualizations": {},
        "recommendations": [
            {
                "title": "Otimização de Conteúdo para Palavras-chave Target",
                "description": (
                    f"Identificamos gaps significativos no conteúdo do site para as palavras-chave principais. "
                    f"Recomendamos a criação de conteúdo otimizado focado nas palavras-chave com maior potencial "
                    f"de conversão e menor competição."
                ),
                "action_items": [
                    "Criar artigos de blog para as 5 palavras-chave prioritárias",
                    "Otimizar metadados (títulos, descrições) das páginas principais",
                    "Desenvolver landing pages específicas para cada segmento de cliente"
                ]
            },
            {
                "title": "Melhorias Técnicas de SEO",
                "description": (
                    f"Nossa análise técnica do site {website_url} identificou problemas que afetam o rankeamento "
                    f"nos motores de busca, incluindo tempo de carregamento, responsividade em dispositivos móveis "
                    f"e estrutura de URLs."
                ),
                "action_items": [
                    "Otimizar a velocidade de carregamento do site",
                    "Implementar URLs amigáveis aos motores de busca",
                    "Corrigir problemas de indexação e rastreamento"
                ]
            },
            {
                "title": "Estratégia de Link Building",
                "description": (
                    f"Em comparação com os concorrentes ({competitors}), identificamos uma deficiência "
                    f"em backlinks de qualidade. Recomendamos uma estratégia específica para aumentar a "
                    f"autoridade do domínio e melhorar o posicionamento orgânico."
                ),
                "action_items": [
                    "Desenvolver conteúdo de alto valor para atrair links naturais",
                    "Estabelecer parcerias com sites relevantes do setor",
                    "Monitorar e desavowar links tóxicos"
                ]
            }
        ],
        "conclusion": (
            f"A análise SEO de {business_name} revela oportunidades significativas para melhorar a visibilidade online "
            f"e alcançar os objetivos estabelecidos. Implementando as recomendações deste relatório de forma sistemática, "
            f"estimamos um potencial de aumento de 30-40% no tráfego orgânico nos próximos 3-6 meses, com consequente "
            f"impacto positivo nas conversões. Recomendamos um monitoramento contínuo de métricas-chave para ajustar "
            f"a estratégia conforme necessário."
        ),
        "form_data": form_data
    }
    
    # Generate visualizations
    # 1. Keyword Performance
    keywords_list = [kw.strip() for kw in keywords.split(',')]
    if len(keywords_list) < 5:  # Ensure at least 5 keywords for visualization
        keywords_list.extend([f"keyword{i}" for i in range(len(keywords_list), 5)])
    
    positions = [random.randint(5, 30) for _ in range(len(keywords_list))]
    search_volume = [random.randint(100, 5000) for _ in range(len(keywords_list))]
    
    keyword_performance = px.scatter(
        x=keywords_list,
        y=positions,
        size=search_volume,
        color=keywords_list,
        title="Performance de Palavras-chave",
        labels={'x': 'Palavras-chave', 'y': 'Posição nos Resultados de Busca'},
    )
    
    keyword_performance.update_yaxes(autorange="reversed")  # Reverse y-axis so lower numbers (better rankings) are at top
    
    # 2. Traffic Sources
    sources = ['Orgânico', 'Direto', 'Redes Sociais', 'Referral', 'Email']
    traffic_values = [random.randint(20, 60), random.randint(10, 30), random.randint(5, 20), random.randint(5, 15), random.randint(1, 10)]
    
    traffic_sources = px.pie(
        values=traffic_values,
        names=sources,
        title="Fontes de Tráfego",
    )
    
    # 3. Optimization Opportunities
    opportunities = ['Conteúdo', 'Técnico', 'Link Building', 'Local SEO', 'Mobile']
    impact_values = [random.randint(60, 90), random.randint(40, 80), random.randint(50, 70), random.randint(30, 60), random.randint(50, 90)]
    difficulty_values = [random.randint(20, 60), random.randint(40, 70), random.randint(50, 80), random.randint(10, 40), random.randint(30, 50)]
    
    optimization_opportunities = px.scatter(
        x=difficulty_values,
        y=impact_values,
        text=opportunities,
        size=[40] * len(opportunities),
        title="Matriz de Oportunidades de Otimização",
        labels={'x': 'Dificuldade de Implementação', 'y': 'Impacto Potencial'},
    )
    
    optimization_opportunities.update_traces(textposition='top center')
    
    # Add visualizations to report
    report['visualizations'] = {
        'keyword_performance': keyword_performance,
        'traffic_sources': traffic_sources,
        'optimization_opportunities': optimization_opportunities
    }
    
    return report

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
