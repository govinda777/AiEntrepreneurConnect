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
    expect(page.get_by_role("heading", name="Mapa do Seu Negócio", exact=True)).to_be_visible()
    
    # Fill in form fields with Xperience data
    page.get_by_label("Nome da empresa").fill("Xperience")
    page.get_by_label("Setor de atuação").fill("Tecnologia")
    page.get_by_label("Modelo de negócio").fill("Consultoria")
    page.get_by_label("Faturamento mensal médio (R$)").fill("50000")
    page.get_by_label("Número de colaboradores").fill("10")
    page.get_by_label("Principais produtos/serviços (separados por vírgula)").fill("Consultoria em transformação digital, Desenvolvimento de software, Treinamentos")
    page.get_by_label("Público-alvo").fill("Pequenas e médias empresas do setor de tecnologia")
    page.get_by_label("Principais concorrentes (separados por vírgula)").fill("Empresa A, Empresa B, Empresa C")
    
    # Submit form
    page.get_by_role("button", name="Gerar Mapa do Seu Negócio").click()
    
    # Check for success message
    expect(page.get_by_text("Gerando seu relatório... Por favor, aguarde.")).to_be_visible()

def test_blue_ocean_form(page: Page, base_url):
    """Test the blue ocean form functionality"""
    page.goto(base_url)
    
    # Connect wallet
    page.get_by_role("button", name="Metamask").click()
    
    # Navigate to blue ocean form
    page.get_by_role("button", name="Gerar Xperience").click()
    
    # Check form elements
    expect(page.get_by_role("heading", name="Relatório Xperience (Blue Ocean)", exact=True)).to_be_visible()
    
    # Fill in form fields
    page.get_by_label("Nome da empresa").fill("Xperience")
    page.get_by_label("Produtos/Serviços atuais").fill("Consultoria em transformação digital, Desenvolvimento de software, Treinamentos")
    page.get_by_label("Principais concorrentes (separados por vírgula)").fill("Empresa A, Empresa B, Empresa C")
    page.get_by_label("Cliente-alvo").fill("Pequenas e médias empresas do setor de tecnologia")
    page.get_by_label("Diferenciais competitivos atuais").fill("Preço acessível, Atendimento personalizado, Tecnologia proprietária")
    page.get_by_label("Principais desafios do negócio").fill("Alta competição por preço, Dificuldade de aquisição de clientes")
    page.get_by_label("Objetivos estratégicos").fill("Expandir para novos mercados, Aumentar margem de lucro")
    page.get_by_label("Principais pontos fortes").fill("Equipe qualificada, Tecnologia proprietária")
    page.get_by_label("Principais limitações").fill("Orçamento limitado, Equipe pequena")
    
    # Submit form
    page.get_by_role("button", name="Gerar Relatório Xperience").click()
    
    # Check for success message
    expect(page.get_by_text("Gerando seu relatório... Por favor, aguarde.")).to_be_visible()

def test_seo_form(page: Page, base_url):
    """Test the SEO form functionality"""
    page.goto(base_url)
    
    # Connect wallet
    page.get_by_role("button", name="Metamask").click()
    
    # Navigate to SEO form
    page.get_by_role("button", name="Gerar SEO").click()
    
    # Check form elements
    expect(page.get_by_role("heading", name="Relatório SEO", exact=True)).to_be_visible()
    
    # Fill in form fields with Xperience data
    page.get_by_label("Nome da empresa").fill("Xperience")
    page.get_by_label("URL do site").fill("https://xperiencehubs.com")
    page.get_by_label("Palavras-chave").fill("consultoria empresarial, DAO, oceano azul, transformação digital, inovação descentralizada")
    
    # Submit form
    page.get_by_role("button", name="Gerar Relatório SEO").click()
    
    # Check for success message
    expect(page.get_by_text("Gerando seu relatório... Por favor, aguarde.")).to_be_visible() 