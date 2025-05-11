import pytest
from playwright.sync_api import Page, expect
import time

def test_landing_page(page: Page, base_url):
    """Test the landing page loads correctly and displays expected content"""
    # Configura um timeout maior para a navegação
    page.set_default_timeout(60000)  # 60 segundos
    
    # Navega para a página
    page.goto(base_url)
    
    # Aguarda a página carregar completamente
    page.wait_for_load_state("networkidle")
    page.wait_for_load_state("domcontentloaded")
    
    # Aguarda o spinner do Streamlit desaparecer
    page.wait_for_selector(".stSpinner", state="hidden", timeout=60000)
    
    # Aguarda elementos específicos aparecerem
    page.wait_for_selector("button:has-text('Metamask')", timeout=60000)
    page.wait_for_selector("button:has-text('WalletConnect')", timeout=60000)
    
    # Verifica se os elementos estão visíveis
    expect(page.get_by_role("button", name="Metamask")).to_be_visible()
    expect(page.get_by_role("button", name="WalletConnect")).to_be_visible()
    
    # Verifica se o texto de boas-vindas está presente
    expect(page.get_by_text("Bem-vindo à IA do Empreendedor", exact=False)).to_be_visible()
    
    # Captura de tela para debug
    page.screenshot(path="debug_screenshot.png")
    
    # Verifica o conteúdo da página usando uma abordagem mais flexível
    page_content = page.content()
    assert "IA do Empreendedor" in page_content, "Título não encontrado na página"
    assert "Transformando dados em estratégia para seu negócio" in page_content, "Subtítulo não encontrado na página"
    assert "Metamask" in page_content, "Botão Metamask não encontrado na página"
    assert "WalletConnect" in page_content, "Botão WalletConnect não encontrado na página"
    assert "Bem-vindo à IA do Empreendedor" in page_content, "Mensagem de boas-vindas não encontrada na página"
    
    # Check if the subtitle is visible
    expect(page.get_by_text("Transformando dados em estratégia para seu negócio", exact=False)).to_be_visible(timeout=20000)
    
    # Check if wallet connection buttons are present
    expect(page.get_by_role("button", name="Metamask")).to_be_visible(timeout=20000)
    expect(page.get_by_role("button", name="WalletConnect")).to_be_visible(timeout=20000)
    
    # Check if the welcome message is visible
    expect(page.get_by_text("Bem-vindo à IA do Empreendedor", exact=False)).to_be_visible(timeout=20000)

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