import pytest
import streamlit as st
from report_generator import generate_report
import plotly.graph_objects as go
import plotly.express as px

@pytest.fixture
def sample_business_map_data():
    return {
        'business_name': 'Test Company',
        'industry': 'Technology',
        'business_model': 'SaaS',
        'monthly_revenue': 100000,
        'employees': 10,
        'main_products': 'Software',
        'target_audience': 'SMBs'
    }

@pytest.fixture
def sample_blue_ocean_data():
    return {
        'business_name': 'Test Marketing',
        'products_services': 'Digital Marketing',
        'competitors': 'CompA, CompB',
        'target_customers': 'Tech Startups',
        'differentials': 'Data-Driven Marketing',
        'goals': 'Market Expansion'
    }

@pytest.fixture
def sample_seo_data():
    return {
        'business_name': 'Test Shop',
        'website_url': 'https://testshop.com',
        'keywords': 'test, e-commerce',
        'competitors': 'comp1.com, comp2.com',
        'goals': 'Increase Traffic',
        'channels': 'Google, Social'
    }

def test_business_map_report_generation(sample_business_map_data):
    """Test if business map report is generated correctly with all required fields"""
    report = generate_report('business_map', sample_business_map_data)
    
    # Validate basic report structure
    assert report['id'] is not None
    assert report['generated_date'] is not None
    assert report['report_type'] == 'business_map'
    assert report['report_type_display'] == 'Mapa do Seu Negócio'
    assert report['form_data'] == sample_business_map_data
    
    # Validate report specific content
    assert report['title'] == f"Mapa Estratégico: {sample_business_map_data['business_name']}"
    assert 'executive_summary' in report
    
    # Validate visualizations
    visualizations = report['visualizations']
    assert 'radar_chart' in visualizations
    assert 'market_comparison' in visualizations
    assert 'growth_potential' in visualizations
    
    # Validate chart types
    assert isinstance(visualizations['radar_chart'], go.Figure)
    assert isinstance(visualizations['market_comparison'], go.Figure)
    assert isinstance(visualizations['growth_potential'], go.Figure)

def test_blue_ocean_report_generation(sample_blue_ocean_data):
    """Test if blue ocean report is generated correctly with all required fields"""
    report = generate_report('blue_ocean', sample_blue_ocean_data)
    
    # Validate basic report structure
    assert report['id'] is not None
    assert report['generated_date'] is not None
    assert report['report_type'] == 'blue_ocean'
    assert report['report_type_display'] == 'Relatório Xperience (Blue Ocean)'
    assert report['form_data'] == sample_blue_ocean_data
    
    # Validate report specific content
    assert report['title'] == f"Estratégia Blue Ocean: {sample_blue_ocean_data['business_name']}"
    assert 'executive_summary' in report
    
    # Validate visualizations
    visualizations = report['visualizations']
    assert 'strategy_canvas' in visualizations
    assert 'actions_chart' in visualizations
    assert 'performance_projection' in visualizations
    
    # Validate chart types
    assert isinstance(visualizations['strategy_canvas'], go.Figure)
    assert isinstance(visualizations['actions_chart'], go.Figure)
    assert isinstance(visualizations['performance_projection'], go.Figure)

def test_seo_report_generation(sample_seo_data):
    """Test if SEO report is generated correctly with all required fields"""
    report = generate_report('seo', sample_seo_data)
    
    # Validate basic report structure
    assert report['id'] is not None
    assert report['generated_date'] is not None
    assert report['report_type'] == 'seo'
    assert report['report_type_display'] == 'Relatório SEO'
    assert report['form_data'] == sample_seo_data
    
    # Validate report specific content
    assert report['title'] == f"Análise SEO: {sample_seo_data['business_name']}"
    assert 'executive_summary' in report
    
    # Validate visualizations
    visualizations = report['visualizations']
    assert 'keyword_performance' in visualizations
    assert 'traffic_sources' in visualizations
    assert 'optimization_opportunities' in visualizations
    
    # Validate chart types
    assert isinstance(visualizations['keyword_performance'], go.Figure)
    assert isinstance(visualizations['traffic_sources'], go.Figure)
    assert isinstance(visualizations['optimization_opportunities'], go.Figure)

def test_invalid_report_type():
    """Test if invalid report type raises ValueError"""
    with pytest.raises(ValueError) as exc_info:
        generate_report('invalid_type', {})
    assert 'Tipo de relatório inválido' in str(exc_info.value)

def test_visualization_parameters(sample_business_map_data):
    """Test if visualizations are created with correct parameters"""
    report = generate_report('business_map', sample_business_map_data)
    
    # Test market comparison chart
    market_comparison = report['visualizations']['market_comparison']
    assert market_comparison.layout.title.text == "Comparação com o Mercado"
    assert market_comparison.layout.xaxis.title.text == "Categorias"
    assert market_comparison.layout.yaxis.title.text == "Valores"
    
    # Test growth potential chart
    growth_potential = report['visualizations']['growth_potential']
    assert growth_potential.layout.title.text == "Potencial de Crescimento"
    assert growth_potential.layout.xaxis.title.text == "Período"
    assert growth_potential.layout.yaxis.title.text == "Crescimento (%)"

def test_empty_data_handling():
    """Test if report generation handles empty or missing data gracefully"""
    empty_data = {'business_name': 'Test Company'}  # Minimal required data
    
    report = generate_report('business_map', empty_data)
    
    # Validate that visualizations are created even with empty data
    visualizations = report['visualizations']
    assert 'radar_chart' in visualizations
    assert 'market_comparison' in visualizations
    assert 'growth_potential' in visualizations
    
    # Validate that charts are created with default/empty values
    market_comparison = visualizations['market_comparison']
    assert len(market_comparison.data) > 0  # Chart should exist even if empty 