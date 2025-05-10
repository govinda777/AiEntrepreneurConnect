import pytest
from playwright.sync_api import Page, expect

def test_landing_page(page: Page, base_url):
    """Test the landing page loads correctly and displays expected content"""
    page.goto(base_url)
    
    # Check if the main title is visible
    expect(page.get_by_role("heading", name="IA do Empreendedor", exact=True)).to_be_visible()
    
    # Check if the subtitle is visible
    expect(page.get_by_text("Transformando dados em estratégia para seu negócio")).to_be_visible()
    
    # Check if wallet connection buttons are present
    expect(page.get_by_role("button", name="Metamask")).to_be_visible()
    expect(page.get_by_role("button", name="WalletConnect")).to_be_visible()
    
    # Check if the welcome message is visible
    expect(page.get_by_text("Bem-vindo à IA do Empreendedor")).to_be_visible()

def test_navigation_after_wallet_connection(page: Page, base_url):
    """Test navigation after wallet connection"""
    page.goto(base_url)
    
    # Click the Metamask button (Note: In a real test, you'd need to handle the wallet connection)
    page.get_by_role("button", name="Metamask").click()
    
    # Wait for the dashboard to appear
    expect(page.get_by_text("Gerar Novo Relatório")).to_be_visible()
    
    # Check if all tabs are present
    expect(page.get_by_role("tab", name="Gerar Novo Relatório")).to_be_visible()
    expect(page.get_by_role("tab", name="Meus Relatórios")).to_be_visible()
    expect(page.get_by_role("tab", name="Dashboard Metro")).to_be_visible()

def test_report_generation_flow(page: Page, base_url):
    """Test the report generation flow"""
    page.goto(base_url)
    
    # Click the Metamask button (Note: In a real test, you'd need to handle the wallet connection)
    page.get_by_role("button", name="Metamask").click()
    
    # Wait for the dashboard and click on "Gerar Mapa"
    page.get_by_role("button", name="Gerar Mapa").click()
    
    # Check if we're on the form page
    expect(page.get_by_role("heading", name="Mapa do Seu Negócio", exact=True)).to_be_visible()
    
    # Check if the back button is present
    expect(page.get_by_role("button", name="← Voltar para o Dashboard")).to_be_visible() 