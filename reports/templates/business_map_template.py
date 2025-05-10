from typing import Dict, Any
from .base_template import ReportTemplate

class BusinessMapTemplate(ReportTemplate):
    """Template específico para relatórios de Business Map"""
    
    def format_executive_summary(self, data: Dict[str, Any]) -> str:
        business_name = data.get('business_name', 'Empresa')
        industry = data.get('industry', 'Tecnologia')
        business_model = data.get('business_model', 'SaaS')
        monthly_revenue = data.get('monthly_revenue', 0)
        employees = data.get('employees', 0)
        
        return (
            f"{business_name} atua no setor de {industry} com um modelo de negócio {business_model}. "
            f"Com um faturamento mensal de R$ {monthly_revenue:,.2f} e {employees} colaboradores, "
            f"a empresa demonstra potencial para crescimento em áreas específicas, conforme detalhado neste relatório."
        )
    
    def format_main_content(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "swot_analysis": {
                "strengths": data.get('strengths', []),
                "weaknesses": data.get('weaknesses', []),
                "opportunities": data.get('opportunities', []),
                "threats": data.get('threats', [])
            },
            "market_analysis": data.get('market_analysis', {}),
            "competitive_analysis": data.get('competitive_analysis', {})
        }
    
    def format_recommendations(self, data: Dict[str, Any]) -> list:
        recommendations = data.get('recommendations', [])
        # Garante que cada recomendação tem a estrutura esperada
        formatted_recommendations = []
        for rec in recommendations:
            if isinstance(rec, dict):
                formatted_recommendations.append({
                    "title": rec.get('title', ''),
                    "description": rec.get('description', ''),
                    "action_items": rec.get('action_items', [])
                })
        return formatted_recommendations
    
    def format_visualizations(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "radar_chart": data.get('radar_chart', {}),
            "market_position": data.get('market_position', {}),
            "growth_trajectory": data.get('growth_trajectory', {})
        } 