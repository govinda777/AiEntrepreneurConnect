import pytest
from playwright.sync_api import Page, expect

def test_business_map_form(page: Page, base_url):
    """Test the business map form functionality"""
    page.goto(base_url)
    
    # Connect wallet (Note: In a real test, you'd need to handle the wallet connection)
    page.get_by_role("button", name="Metamask").click()
    
    # Navigate to business map form
    page.get_by_role("button", name="Gerar Mapa").click()
    
    # Check form elements
    expect(page.get_by_role("heading", name="Mapa do Seu Negócio")).to_be_visible()
    
    # Fill in form fields with Xperience data
    page.get_by_label("Nome da Empresa").fill("Xperience")
    page.get_by_label("Setor").select_option("Consultoria")
    page.get_by_label("Faturamento Mensal").fill("50000")
    
    # Submit form
    page.get_by_role("button", name="Gerar Relatório").click()
    
    # Check for success message or report generation
    expect(page.get_by_text("Gerando seu relatório").first()).to_be_visible()

def test_blue_ocean_form(page: Page, base_url):
    """Test the blue ocean form functionality"""
    page.goto(base_url)
    
    # Connect wallet
    page.get_by_role("button", name="Metamask").click()
    
    # Navigate to blue ocean form
    page.get_by_role("button", name="Gerar Xperience").click()
    
    # Check form elements
    expect(page.get_by_role("heading", name="Relatório Xperience (Blue Ocean)")).to_be_visible()
    
    # Fill in form fields with Xperience data
    page.get_by_label("Nome da Empresa").fill("Xperience")
    page.get_by_label("Setor").select_option("Consultoria")
    page.get_by_label("Objetivo").fill("Revolucionar o mercado de consultoria empresarial através de metodologias inovadoras e tecnologia descentralizada")
    
    # Submit form
    page.get_by_role("button", name="Gerar Relatório").click()
    
    # Check for success message or report generation
    expect(page.get_by_text("Gerando seu relatório").first()).to_be_visible()

def test_seo_form(page: Page, base_url):
    """Test the SEO form functionality"""
    page.goto(base_url)
    
    # Connect wallet
    page.get_by_role("button", name="Metamask").click()
    
    # Navigate to SEO form
    page.get_by_role("button", name="Gerar SEO").click()
    
    # Check form elements
    expect(page.get_by_role("heading", name="Relatório SEO")).to_be_visible()
    
    # Fill in form fields with Xperience data
    page.get_by_label("URL do Site").fill("https://xperiencehubs.com")
    page.get_by_label("Palavras-chave").fill("consultoria empresarial, DAO, oceano azul, transformação digital, inovação descentralizada")
    
    # Submit form
    page.get_by_role("button", name="Gerar Relatório").click()
    
    # Check for success message or report generation
    expect(page.get_by_text("Gerando seu relatório").first()).to_be_visible() 