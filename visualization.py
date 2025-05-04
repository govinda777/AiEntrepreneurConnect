import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def create_radar_chart(categories, values, title):
    """Create a radar chart for business areas"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Seu Negócio'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        title=title
    )
    
    return fig

def create_strategy_canvas(factors, your_values, competitor_values):
    """Create a strategy canvas comparing your business with competitors"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=factors,
        y=your_values,
        mode='lines+markers',
        name='Sua Empresa',
        line=dict(color='blue', width=4)
    ))
    
    fig.add_trace(go.Scatter(
        x=factors,
        y=competitor_values,
        mode='lines+markers',
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

def create_errc_chart():
    """Create a chart for the Eliminate-Reduce-Raise-Create framework"""
    actions = ["Eliminar", "Reduzir", "Aumentar", "Criar"]
    colors = ['#FF6347', '#FFA500', '#3CB371', '#4682B4']
    
    fig = go.Figure()
    
    for i, action in enumerate(actions):
        fig.add_trace(go.Bar(
            x=[action],
            y=[1],
            name=action,
            marker_color=colors[i],
            text=action,
            textposition='auto',
            width=0.8
        ))
    
    fig.update_layout(
        title="Framework das Quatro Ações (ERRC)",
        showlegend=False,
        xaxis=dict(title="Ações Estratégicas"),
        yaxis=dict(
            title="",
            showticklabels=False,
            showgrid=False
        ),
        height=300
    )
    
    return fig

def create_keyword_performance(keywords, positions, search_volumes):
    """Create a scatter plot for keyword performance"""
    df = pd.DataFrame({
        'Palavra-chave': keywords,
        'Posição': positions,
        'Volume de Busca': search_volumes
    })
    
    fig = px.scatter(
        df, 
        x='Palavra-chave', 
        y='Posição',
        size='Volume de Busca',
        color='Palavra-chave',
        title="Performance de Palavras-chave",
        labels={'Posição': 'Posição no Google'}
    )
    
    # Reverse y-axis so that position 1 is at the top
    fig.update_yaxes(autorange="reversed")
    
    return fig

def create_traffic_sources_chart(sources, percentages):
    """Create a pie chart for traffic sources"""
    df = pd.DataFrame({
        'Fonte': sources,
        'Porcentagem': percentages
    })
    
    fig = px.pie(
        df,
        values='Porcentagem',
        names='Fonte',
        title='Fontes de Tráfego',
        hole=0.4
    )
    
    return fig

def create_optimization_matrix(areas, impact, difficulty):
    """Create a scatter plot for SEO optimization opportunities"""
    df = pd.DataFrame({
        'Área': areas,
        'Impacto': impact,
        'Dificuldade': difficulty
    })
    
    fig = px.scatter(
        df,
        x='Dificuldade',
        y='Impacto',
        text='Área',
        size=[40] * len(areas),
        color='Área',
        title="Matriz de Oportunidades de Otimização",
        labels={
            'Dificuldade': 'Dificuldade de Implementação',
            'Impacto': 'Impacto Potencial'
        }
    )
    
    fig.update_traces(textposition='top center')
    
    return fig

def create_comparison_bar_chart(categories, values, competitor_values, title):
    """Create a bar chart comparing your business with competitors"""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        name='Sua Empresa',
        marker_color='rgb(55, 83, 109)'
    ))
    
    fig.add_trace(go.Bar(
        x=categories,
        y=competitor_values,
        name='Média do Mercado',
        marker_color='rgb(26, 118, 255)'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Categorias",
        yaxis_title="Valores",
        barmode='group'
    )
    
    return fig

def create_projection_chart(periods, your_values, market_values):
    """Create a line chart for business projections"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=periods,
        y=your_values,
        mode='lines+markers',
        name='Sua Empresa',
        line=dict(color='blue', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=periods,
        y=market_values,
        mode='lines+markers',
        name='Mercado Tradicional',
        line=dict(color='red', width=3)
    ))
    
    fig.update_layout(
        title="Projeção de Crescimento",
        xaxis_title="Período",
        yaxis_title="Crescimento (%)"
    )
    
    return fig
