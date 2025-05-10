import uuid
import datetime
from templates.business_map_template import BusinessMapTemplate
from prompts.business_map_prompt import BusinessMapPrompt
from llm_configs.business_map_llm import BusinessMapLLM

def generate_business_map_report(form_data: dict) -> dict:
    """
    Exemplo de como gerar um relatório de Business Map usando
    os três componentes: Template, Prompt e LLM.
    """
    
    # Cria instâncias dos componentes
    template = BusinessMapTemplate(
        report_id=str(uuid.uuid4()),
        generated_date=datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    )
    prompt = BusinessMapPrompt()
    llm = BusinessMapLLM()
    
    # Obtém os prompts formatados
    prompts = prompt.get_prompts(form_data)
    
    # Gera a análise usando o LLM
    analysis = llm.generate_analysis(prompts, form_data)
    
    # Gera recomendações baseadas na análise
    recommendations = llm.generate_recommendations(prompts, analysis)
    
    # Combina os dados para o template
    report_data = {
        **form_data,
        **analysis,
        'recommendations': recommendations
    }
    
    # Valida os dados de saída
    if not llm.validate_output(report_data):
        raise ValueError("Os dados gerados não estão no formato esperado")
    
    # Gera o relatório final usando o template
    report = template.generate(report_data)
    
    return report

# Exemplo de uso
if __name__ == "__main__":
    # Dados de exemplo
    form_data = {
        "business_name": "TechCorp Solutions",
        "industry": "Software",
        "business_model": "SaaS",
        "monthly_revenue": 100000.00,
        "employees": 15
    }
    
    try:
        # Gera o relatório
        report = generate_business_map_report(form_data)
        
        # Imprime o resultado
        print("Relatório gerado com sucesso!")
        print(f"ID: {report['id']}")
        print(f"Data: {report['generated_date']}")
        print("\nSumário Executivo:")
        print(report['executive_summary'])
        
    except Exception as e:
        print(f"Erro ao gerar relatório: {e}") 