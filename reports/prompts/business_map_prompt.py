from typing import Dict, Any
from .base_prompt import ReportPrompt

class BusinessMapPrompt(ReportPrompt):
    """Prompts específicos para relatórios de Business Map"""
    
    def get_system_prompt(self) -> str:
        return """Você é um consultor estratégico especializado em análise de negócios.
        Sua função é analisar dados de empresas e gerar insights valiosos e acionáveis.
        Suas análises devem ser:
        1. Objetivas e baseadas em dados
        2. Estratégicas e orientadas para resultados
        3. Práticas e implementáveis
        4. Específicas para o contexto do negócio
        
        Mantenha um tom profissional e construtivo em todas as análises."""
    
    def format_user_prompt(self, data: Dict[str, Any]) -> str:
        business_name = data.get('business_name', 'Empresa')
        industry = data.get('industry', 'Tecnologia')
        business_model = data.get('business_model', 'SaaS')
        
        return f"""Analise os seguintes dados da empresa {business_name}:
        
        Setor: {industry}
        Modelo de Negócio: {business_model}
        
        Considere:
        1. Posicionamento atual no mercado
        2. Principais diferenciais competitivos
        3. Oportunidades de crescimento
        4. Riscos e desafios
        
        Forneça uma análise detalhada que inclua:
        - Análise SWOT completa
        - Análise de mercado
        - Análise competitiva"""
    
    def format_analysis_prompt(self, data: Dict[str, Any]) -> str:
        monthly_revenue = data.get('monthly_revenue', 0)
        employees = data.get('employees', 0)
        
        return f"""Com base nos seguintes indicadores:
        
        Faturamento Mensal: R$ {monthly_revenue:,.2f}
        Número de Funcionários: {employees}
        
        Analise:
        1. Eficiência operacional
        2. Potencial de escalabilidade
        3. Necessidades de investimento
        4. Áreas prioritárias para desenvolvimento
        
        Forneça insights específicos e métricas comparativas com o mercado."""
    
    def format_recommendations_prompt(self, data: Dict[str, Any]) -> str:
        return """Com base na análise anterior, forneça:
        
        1. 3-5 recomendações estratégicas principais
        2. Para cada recomendação:
           - Título claro e objetivo
           - Descrição detalhada do problema/oportunidade
           - 3-5 ações práticas para implementação
        
        As recomendações devem ser:
        - Específicas e acionáveis
        - Priorizadas por impacto e facilidade de implementação
        - Alinhadas com os recursos e capacidades atuais da empresa""" 