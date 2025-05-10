from typing import Dict, Any
from .base_llm import ReportLLM, LLMConfig
import json

class BusinessMapLLM(ReportLLM):
    """Configuração específica do LLM para relatórios de Business Map"""
    
    def __init__(self):
        config = LLMConfig(
            model_name="gpt-4-turbo-preview",  # Modelo mais recente para análises complexas
            temperature=0.7,  # Balanceando criatividade com consistência
            max_tokens=4000,  # Limite adequado para análises detalhadas
            top_p=0.9,  # Mantendo diversidade nas respostas
            frequency_penalty=0.3,  # Evitando repetições
            presence_penalty=0.3  # Incentivando diversidade
        )
        super().__init__(config)
    
    def generate_analysis(self, prompts: Dict[str, str], data: Dict[str, Any]) -> Dict[str, Any]:
        # Combina os prompts do sistema e usuário para análise inicial
        analysis_prompt = f"""{prompts['system']}
        
        {prompts['user']}
        
        {prompts['analysis']}"""
        
        # Obtém a resposta do LLM
        response = self.get_completion(analysis_prompt)
        if not response:
            return {}
            
        try:
            # Tenta estruturar a resposta em um formato consistente
            analysis = {
                "swot_analysis": {
                    "strengths": [],
                    "weaknesses": [],
                    "opportunities": [],
                    "threats": []
                },
                "market_analysis": {},
                "competitive_analysis": {}
            }
            
            # Aqui seria implementada a lógica de parsing da resposta do LLM
            # para preencher a estrutura de análise
            
            return analysis
            
        except Exception as e:
            print(f"Error parsing analysis response: {e}")
            return {}
    
    def generate_recommendations(self, prompts: Dict[str, str], analysis: Dict[str, Any]) -> list:
        # Combina a análise anterior com o prompt de recomendações
        recommendations_prompt = f"""{prompts['system']}
        
        Análise prévia:
        {json.dumps(analysis, indent=2)}
        
        {prompts['recommendations']}"""
        
        # Obtém a resposta do LLM
        response = self.get_completion(recommendations_prompt)
        if not response:
            return []
            
        try:
            # Estrutura as recomendações em um formato consistente
            recommendations = []
            # Aqui seria implementada a lógica de parsing da resposta do LLM
            # para estruturar as recomendações
            return recommendations
            
        except Exception as e:
            print(f"Error parsing recommendations response: {e}")
            return []
    
    def validate_output(self, output: Dict[str, Any]) -> bool:
        """
        Valida se a saída contém todos os elementos necessários
        para um relatório de Business Map completo.
        """
        required_keys = [
            'swot_analysis',
            'market_analysis',
            'competitive_analysis',
            'recommendations'
        ]
        
        # Verifica se todas as chaves necessárias estão presentes
        for key in required_keys:
            if key not in output:
                return False
                
        # Verifica se a análise SWOT está completa
        swot = output.get('swot_analysis', {})
        swot_components = ['strengths', 'weaknesses', 'opportunities', 'threats']
        for component in swot_components:
            if component not in swot or not isinstance(swot[component], list):
                return False
                
        # Verifica se há recomendações e se estão no formato correto
        recommendations = output.get('recommendations', [])
        if not recommendations or not isinstance(recommendations, list):
            return False
            
        for rec in recommendations:
            if not isinstance(rec, dict) or \
               'title' not in rec or \
               'description' not in rec or \
               'action_items' not in rec:
                return False
                
        return True 