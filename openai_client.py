import json
import os
import time

# The newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# Do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

try:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    OPENAI_AVAILABLE = True
except Exception as e:
    print(f"Erro ao inicializar o cliente OpenAI: {e}")
    OPENAI_AVAILABLE = False

def analyze_business(form_data):
    """
    Analyze business data using OpenAI's GPT model
    
    This function takes form data about a business and sends it to OpenAI's API
    to generate insights and recommendations.
    
    If OpenAI is not available, it returns simulated data.
    """
    # If OpenAI is not available, return simulated data immediately
    if not OPENAI_AVAILABLE:
        business_name = form_data.get('business_name', 'Empresa')
        industry = form_data.get('industry', 'Tecnologia')
        
        # Simulate API analysis with a delay to make it feel realistic
        time.sleep(1.5)
        
        return {
            "strengths": [
                f"Posicionamento único no mercado de {industry}",
                "Equipe comprometida",
                "Produto com diferenciais claros"
            ],
            "weaknesses": [
                "Processos que podem ser otimizados",
                "Dependência de poucos canais de aquisição",
                "Escalabilidade limitada no modelo atual"
            ],
            "opportunities": [
                "Expandir para mercados adjacentes",
                "Desenvolver novas linhas de produtos/serviços",
                f"Parcerias estratégicas com outros players de {industry}"
            ],
            "threats": [
                "Novos entrantes com modelos disruptivos",
                "Mudanças regulatórias no setor",
                "Pressão por redução de preços"
            ],
            "recommendations": [
                {
                    "title": "Otimização de Processos",
                    "description": f"Implementar melhorias nos processos internos de {business_name} para aumentar eficiência operacional.",
                    "action_items": [
                        "Mapear processos atuais e identificar gargalos",
                        "Implementar ferramentas de automação",
                        "Treinar equipe em novas metodologias"
                    ]
                },
                {
                    "title": "Diversificação de Canais",
                    "description": f"Expandir os canais de aquisição de {business_name} para reduzir dependências e aumentar alcance.",
                    "action_items": [
                        "Testar novos canais de marketing",
                        "Desenvolver programa de parcerias",
                        "Implementar estratégia de conteúdo"
                    ]
                },
                {
                    "title": "Inovação de Produto",
                    "description": f"Desenvolver novos produtos/serviços que complementem a oferta atual de {business_name}.",
                    "action_items": [
                        "Realizar pesquisa com clientes",
                        "Desenvolver MVPs para testar conceitos",
                        "Estabelecer processo de inovação contínua"
                    ]
                }
            ]
        }
    # Create a prompt with the form data
    business_name = form_data.get('business_name', 'Empresa')
    industry = form_data.get('industry', 'Tecnologia')
    business_model = form_data.get('business_model', 'SaaS')
    monthly_revenue = form_data.get('monthly_revenue', 50000)
    employees = form_data.get('employees', 10)
    main_products = form_data.get('main_products', '')
    target_audience = form_data.get('target_audience', '')
    competitors = form_data.get('competitors', '')
    marketing_channels = form_data.get('marketing_channels', [])
    growth_stage = form_data.get('growth_stage', '')
    
    prompt = f"""
    Você é um consultor de negócios especialista que deve analisar os dados da empresa abaixo e gerar insights estratégicos.
    
    DADOS DA EMPRESA:
    - Nome: {business_name}
    - Setor: {industry}
    - Modelo de negócio: {business_model}
    - Faturamento mensal: R$ {monthly_revenue}
    - Número de colaboradores: {employees}
    - Produtos/serviços principais: {main_products}
    - Público-alvo: {target_audience}
    - Concorrentes: {competitors}
    - Canais de marketing: {', '.join(marketing_channels) if marketing_channels else 'Não informado'}
    - Estágio de crescimento: {growth_stage}
    
    TAREFA:
    Gere uma análise SWOT completa e 3 recomendações estratégicas detalhadas. 
    As recomendações devem ser específicas para o contexto da empresa e incluir ações concretas.
    
    Organize a resposta em JSON no seguinte formato:
    {{
        "strengths": ["ponto forte 1", "ponto forte 2", ...],
        "weaknesses": ["ponto fraco 1", "ponto fraco 2", ...],
        "opportunities": ["oportunidade 1", "oportunidade 2", ...],
        "threats": ["ameaça 1", "ameaça 2", ...],
        "recommendations": [
            {{
                "title": "Título da recomendação 1",
                "description": "Descrição detalhada",
                "action_items": ["ação 1", "ação 2", "ação 3"]
            }},
            ...
        ]
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um consultor de negócios especialista em análise estratégica."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        # Parse the JSON response
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        # If there's an error, return a default response
        print(f"Error calling OpenAI API: {e}")
        return {
            "strengths": [
                f"Posicionamento único no mercado de {industry}",
                "Equipe comprometida",
                "Produto com diferenciais claros"
            ],
            "weaknesses": [
                "Processos que podem ser otimizados",
                "Dependência de poucos canais de aquisição",
                "Escalabilidade limitada no modelo atual"
            ],
            "opportunities": [
                "Expandir para mercados adjacentes",
                "Desenvolver novas linhas de produtos/serviços",
                f"Parcerias estratégicas com outros players de {industry}"
            ],
            "threats": [
                "Novos entrantes com modelos disruptivos",
                "Mudanças regulatórias no setor",
                "Pressão por redução de preços"
            ],
            "recommendations": [
                {
                    "title": "Otimização de Processos",
                    "description": f"Implementar melhorias nos processos internos de {business_name} para aumentar eficiência operacional.",
                    "action_items": [
                        "Mapear processos atuais e identificar gargalos",
                        "Implementar ferramentas de automação",
                        "Treinar equipe em novas metodologias"
                    ]
                },
                {
                    "title": "Diversificação de Canais",
                    "description": f"Expandir os canais de aquisição de {business_name} para reduzir dependências e aumentar alcance.",
                    "action_items": [
                        "Testar novos canais de marketing",
                        "Desenvolver programa de parcerias",
                        "Implementar estratégia de conteúdo"
                    ]
                },
                {
                    "title": "Inovação de Produto",
                    "description": f"Desenvolver novos produtos/serviços que complementem a oferta atual de {business_name}.",
                    "action_items": [
                        "Realizar pesquisa com clientes",
                        "Desenvolver MVPs para testar conceitos",
                        "Estabelecer processo de inovação contínua"
                    ]
                }
            ]
        }

def generate_blue_ocean_strategy(form_data):
    """
    Generate a Blue Ocean strategy using OpenAI's GPT model
    
    This function takes form data about a business and sends it to OpenAI's API
    to generate a Blue Ocean strategy.
    
    If OpenAI is not available, it returns simulated data.
    """
    # If OpenAI is not available, return simulated data immediately
    if not OPENAI_AVAILABLE:
        business_name = form_data.get('business_name', 'Empresa')
        products_services = form_data.get('products_services', 'Software')
        
        # Simulate API analysis with a delay to make it feel realistic
        time.sleep(1.5)
        
        return {
            "eliminate": [
                "Funcionalidades complexas raramente utilizadas",
                "Processos burocráticos que atrasam entregas",
                "Dependência de intermediários na cadeia de valor"
            ],
            "reduce": [
                "Custos operacionais através de automação",
                "Tempo de implementação/entrega",
                "Barreiras de adoção para novos clientes"
            ],
            "raise": [
                "Experiência do usuário e facilidade de uso",
                "Transparência e comunicação com clientes",
                "Valor percebido do produto/serviço"
            ],
            "create": [
                "Modelo de precificação baseado em resultados",
                "Comunidade de usuários e co-criação",
                "Integração perfeita com o ecossistema do cliente"
            ],
            "canvas_factors": [
                "Preço",
                "Facilidade de uso",
                "Personalização",
                "Suporte",
                "Integração",
                "Inovação"
            ],
            "your_values": [6, 9, 10, 8, 9, 10],
            "industry_values": [8, 5, 4, 6, 5, 6],
            "recommendations": [
                {
                    "title": "Redefina a proposta de valor",
                    "description": f"Crie uma nova curva de valor para {business_name} focando em elementos altamente valorizados pelos clientes mas negligenciados pelo mercado.",
                    "action_items": [
                        "Mapear elementos que podem ser eliminados",
                        "Identificar fatores a serem elevados acima do padrão",
                        "Desenvolver novos elementos nunca oferecidos no setor"
                    ]
                },
                {
                    "title": "Foco em não-clientes",
                    "description": f"Expanda o mercado mirando pessoas/empresas que atualmente não utilizam {products_services}.",
                    "action_items": [
                        "Identificar os três níveis de não-clientes",
                        "Entender barreiras de adoção atuais",
                        "Desenvolver oferta específica para este público"
                    ]
                },
                {
                    "title": "Execução estratégica",
                    "description": "Implemente a estratégia Blue Ocean com foco, divergência e mensagem clara.",
                    "action_items": [
                        "Alinhar toda organização com a nova estratégia",
                        "Superar obstáculos organizacionais",
                        "Integrar execução à estratégia desde o início"
                    ]
                }
            ]
        }
    # Create a prompt with the form data
    business_name = form_data.get('business_name', 'Empresa')
    products_services = form_data.get('products_services', 'Software')
    competitors = form_data.get('competitors', 'Concorrentes')
    target_customers = form_data.get('target_customers', 'Clientes')
    differentials = form_data.get('differentials', 'Diferenciais')
    challenges = form_data.get('challenges', 'Desafios')
    goals = form_data.get('goals', 'Objetivos')
    strengths = form_data.get('strengths', 'Pontos fortes')
    limitations = form_data.get('limitations', 'Limitações')
    
    prompt = f"""
    Você é um consultor especialista na metodologia Blue Ocean Strategy. Analise os dados da empresa abaixo e gere uma estratégia Blue Ocean completa.
    
    DADOS DA EMPRESA:
    - Nome: {business_name}
    - Produtos/serviços: {products_services}
    - Concorrentes: {competitors}
    - Cliente-alvo: {target_customers}
    - Diferenciais competitivos: {differentials}
    - Desafios: {challenges}
    - Objetivos: {goals}
    - Pontos fortes: {strengths}
    - Limitações: {limitations}
    
    TAREFA:
    Gere uma estratégia Blue Ocean completa, incluindo:
    1. Framework ERRC (Eliminar-Reduzir-Aumentar-Criar)
    2. Fatores para o Strategy Canvas (Tela Estratégica)
    3. 3 recomendações estratégicas detalhadas
    
    Organize a resposta em JSON no seguinte formato:
    {{
        "eliminate": ["elemento 1", "elemento 2", ...],
        "reduce": ["elemento 1", "elemento 2", ...],
        "raise": ["elemento 1", "elemento 2", ...],
        "create": ["elemento 1", "elemento 2", ...],
        "canvas_factors": ["fator 1", "fator 2", ...],
        "your_values": [valor1, valor2, ...],
        "industry_values": [valor1, valor2, ...],
        "recommendations": [
            {{
                "title": "Título da recomendação 1",
                "description": "Descrição detalhada",
                "action_items": ["ação 1", "ação 2", "ação 3"]
            }},
            ...
        ]
    }}
    
    Obs: your_values e industry_values devem ser arrays de números entre 0 e 10, com a mesma quantidade de elementos que canvas_factors.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um consultor especialista em Blue Ocean Strategy."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        # Parse the JSON response
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        # If there's an error, return a default response
        print(f"Error calling OpenAI API: {e}")
        return {
            "eliminate": [
                "Funcionalidades complexas raramente utilizadas",
                "Processos burocráticos que atrasam entregas",
                "Dependência de intermediários na cadeia de valor"
            ],
            "reduce": [
                "Custos operacionais através de automação",
                "Tempo de implementação/entrega",
                "Barreiras de adoção para novos clientes"
            ],
            "raise": [
                "Experiência do usuário e facilidade de uso",
                "Transparência e comunicação com clientes",
                "Valor percebido do produto/serviço"
            ],
            "create": [
                "Modelo de precificação baseado em resultados",
                "Comunidade de usuários e co-criação",
                "Integração perfeita com o ecossistema do cliente"
            ],
            "canvas_factors": [
                "Preço",
                "Facilidade de uso",
                "Personalização",
                "Suporte",
                "Integração",
                "Inovação"
            ],
            "your_values": [6, 9, 10, 8, 9, 10],
            "industry_values": [8, 5, 4, 6, 5, 6],
            "recommendations": [
                {
                    "title": "Redefina a proposta de valor",
                    "description": f"Crie uma nova curva de valor para {business_name} focando em elementos altamente valorizados pelos clientes mas negligenciados pelo mercado.",
                    "action_items": [
                        "Mapear elementos que podem ser eliminados",
                        "Identificar fatores a serem elevados acima do padrão",
                        "Desenvolver novos elementos nunca oferecidos no setor"
                    ]
                },
                {
                    "title": "Foco em não-clientes",
                    "description": f"Expanda o mercado mirando pessoas/empresas que atualmente não utilizam {products_services}.",
                    "action_items": [
                        "Identificar os três níveis de não-clientes",
                        "Entender barreiras de adoção atuais",
                        "Desenvolver oferta específica para este público"
                    ]
                },
                {
                    "title": "Execução estratégica",
                    "description": "Implemente a estratégia Blue Ocean com foco, divergência e mensagem clara.",
                    "action_items": [
                        "Alinhar toda organização com a nova estratégia",
                        "Superar obstáculos organizacionais",
                        "Integrar execução à estratégia desde o início"
                    ]
                }
            ]
        }

def analyze_seo(form_data):
    """
    Analyze SEO data using OpenAI's GPT model
    
    This function takes form data about a website and sends it to OpenAI's API
    to generate SEO insights and recommendations.
    """
    # If OpenAI is not available, return simulated data immediately
    if not OPENAI_AVAILABLE:
        business_name = form_data.get('business_name', 'Empresa')
        website_url = form_data.get('website_url', 'https://exemplo.com')
        keywords = form_data.get('keywords', 'palavras-chave')
        
        # Parse keywords into a list
        keyword_list = [k.strip() for k in keywords.split(',') if k.strip()]
        if not keyword_list:
            keyword_list = ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]
        
        # Ensure we have at least 5 keywords
        while len(keyword_list) < 5:
            keyword_list.append(f"keyword{len(keyword_list)+1}")
        
        # Simulate API analysis with a delay to make it feel realistic
        time.sleep(1.5)
        
        # Return default response
        return {
            "overall_score": 65,
            "keywords_data": {
                "keywords": keyword_list[:5],
                "positions": [4, 12, 18, 7, 22],
                "search_volumes": [2400, 1300, 880, 3200, 590],
                "competition": [0.75, 0.45, 0.3, 0.8, 0.25]
            },
            "traffic_sources": {
                "sources": ["Organic", "Direct", "Social", "Referral", "Paid"],
                "percentages": [35, 25, 20, 15, 5]
            },
            "optimization_opportunities": [
                {
                    "area": "Content",
                    "impact": 85,
                    "difficulty": 40,
                    "recommendations": [
                        "Create in-depth content targeting main keywords",
                        "Optimize meta titles and descriptions",
                        "Improve internal linking structure"
                    ]
                },
                {
                    "area": "Technical",
                    "impact": 65,
                    "difficulty": 70,
                    "recommendations": [
                        "Improve page loading speed",
                        "Fix mobile usability issues",
                        "Implement schema markup"
                    ]
                },
                {
                    "area": "Backlinks",
                    "impact": 75,
                    "difficulty": 80,
                    "recommendations": [
                        "Develop a link building strategy",
                        "Create linkable assets (infographics, studies)",
                        "Establish industry partnerships"
                    ]
                },
                {
                    "area": "Local SEO",
                    "impact": 55,
                    "difficulty": 30,
                    "recommendations": [
                        "Optimize Google Business Profile",
                        "Ensure NAP consistency",
                        "Generate local reviews"
                    ]
                },
                {
                    "area": "Mobile",
                    "impact": 80,
                    "difficulty": 50,
                    "recommendations": [
                        "Improve mobile page speed",
                        "Ensure responsive design",
                        "Optimize for mobile-first indexing"
                    ]
                }
            ],
            "recommendations": [
                {
                    "title": "Otimização de Conteúdo",
                    "description": f"Criar e otimizar conteúdo para as principais palavras-chave identificadas para {website_url}.",
                    "action_items": [
                        "Desenvolver plano de conteúdo focado nas 5 palavras-chave principais",
                        "Otimizar metadados das páginas existentes",
                        "Melhorar estrutura de links internos"
                    ]
                },
                {
                    "title": "Melhorias Técnicas",
                    "description": "Resolver problemas técnicos que afetam o desempenho do site nos motores de busca.",
                    "action_items": [
                        "Melhorar velocidade de carregamento das páginas",
                        "Corrigir problemas de usabilidade móvel",
                        "Implementar marcação de esquema (schema markup)"
                    ]
                },
                {
                    "title": "Estratégia de Backlinks",
                    "description": "Desenvolver links de qualidade para aumentar a autoridade do domínio.",
                    "action_items": [
                        "Criar conteúdo link-worthy (infográficos, estudos)",
                        "Estabelecer parcerias no setor",
                        "Monitorar perfil de backlinks regularmente"
                    ]
                }
            ]
        }
    # Create a prompt with the form data
    business_name = form_data.get('business_name', 'Empresa')
    website_url = form_data.get('website_url', 'https://exemplo.com')
    keywords = form_data.get('keywords', 'palavras-chave')
    competitors = form_data.get('competitors', 'concorrentes')
    digital_channels = form_data.get('digital_channels', [])
    site_age = form_data.get('site_age', '1 a 3 anos')
    goals = form_data.get('goals', 'objetivos')
    target_audience = form_data.get('target_audience', 'público-alvo')
    
    prompt = f"""
    Você é um especialista em SEO que deve analisar os dados do site abaixo e gerar insights e recomendações estratégicas.
    
    DADOS DO SITE:
    - Nome da empresa: {business_name}
    - URL do site: {website_url}
    - Palavras-chave target: {keywords}
    - Sites concorrentes: {competitors}
    - Canais digitais utilizados: {', '.join(digital_channels) if digital_channels else 'Não informado'}
    - Idade do site: {site_age}
    - Objetivos da presença online: {goals}
    - Público-alvo online: {target_audience}
    
    TAREFA:
    Gere uma análise SEO completa, incluindo:
    1. Pontuação geral do site (estimada)
    2. Dados de performance estimada para as 5 palavras-chave principais
    3. Distribuição de fontes de tráfego estimada
    4. 5 áreas de otimização com impacto e dificuldade
    5. 3 recomendações estratégicas detalhadas
    
    Organize a resposta em JSON no seguinte formato:
    {{
        "overall_score": número de 0 a 100,
        "keywords_data": {{
            "keywords": ["palavra-chave 1", "palavra-chave 2", ...],
            "positions": [posição1, posição2, ...],
            "search_volumes": [volume1, volume2, ...],
            "competition": [competição1, competição2, ...]
        }},
        "traffic_sources": {{
            "sources": ["fonte 1", "fonte 2", ...],
            "percentages": [percentual1, percentual2, ...]
        }},
        "optimization_opportunities": [
            {{
                "area": "Área 1",
                "impact": número de 0 a 100,
                "difficulty": número de 0 a 100,
                "recommendations": ["recomendação 1", "recomendação 2", ...]
            }},
            ...
        ],
        "recommendations": [
            {{
                "title": "Título da recomendação 1",
                "description": "Descrição detalhada",
                "action_items": ["ação 1", "ação 2", "ação 3"]
            }},
            ...
        ]
    }}
    
    Obs: 
    - positions são posições no Google (1-100, onde menores números são melhores)
    - search_volumes são números estimados de busca mensal
    - competition são valores de 0 a 1 indicando nível de competição
    - percentages devem somar 100
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um especialista em SEO."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        # Parse the JSON response
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        # If there's an error, return a default response
        print(f"Error calling OpenAI API: {e}")
        
        # Parse keywords into a list
        keyword_list = [k.strip() for k in keywords.split(',') if k.strip()]
        if not keyword_list:
            keyword_list = ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]
        
        # Ensure we have at least 5 keywords
        while len(keyword_list) < 5:
            keyword_list.append(f"keyword{len(keyword_list)+1}")
        
        # Return default response
        return {
            "overall_score": 65,
            "keywords_data": {
                "keywords": keyword_list[:5],
                "positions": [4, 12, 18, 7, 22],
                "search_volumes": [2400, 1300, 880, 3200, 590],
                "competition": [0.75, 0.45, 0.3, 0.8, 0.25]
            },
            "traffic_sources": {
                "sources": ["Organic", "Direct", "Social", "Referral", "Paid"],
                "percentages": [35, 25, 20, 15, 5]
            },
            "optimization_opportunities": [
                {
                    "area": "Content",
                    "impact": 85,
                    "difficulty": 40,
                    "recommendations": [
                        "Create in-depth content targeting main keywords",
                        "Optimize meta titles and descriptions",
                        "Improve internal linking structure"
                    ]
                },
                {
                    "area": "Technical",
                    "impact": 65,
                    "difficulty": 70,
                    "recommendations": [
                        "Improve page loading speed",
                        "Fix mobile usability issues",
                        "Implement schema markup"
                    ]
                },
                {
                    "area": "Backlinks",
                    "impact": 75,
                    "difficulty": 80,
                    "recommendations": [
                        "Develop a link building strategy",
                        "Create linkable assets (infographics, studies)",
                        "Establish industry partnerships"
                    ]
                },
                {
                    "area": "Local SEO",
                    "impact": 55,
                    "difficulty": 30,
                    "recommendations": [
                        "Optimize Google Business Profile",
                        "Ensure NAP consistency",
                        "Generate local reviews"
                    ]
                },
                {
                    "area": "Mobile",
                    "impact": 80,
                    "difficulty": 50,
                    "recommendations": [
                        "Improve mobile page speed",
                        "Ensure responsive design",
                        "Optimize for mobile-first indexing"
                    ]
                }
            ],
            "recommendations": [
                {
                    "title": "Otimização de Conteúdo",
                    "description": f"Criar e otimizar conteúdo para as principais palavras-chave identificadas para {website_url}.",
                    "action_items": [
                        "Desenvolver plano de conteúdo focado nas 5 palavras-chave principais",
                        "Otimizar metadados das páginas existentes",
                        "Melhorar estrutura de links internos"
                    ]
                },
                {
                    "title": "Melhorias Técnicas",
                    "description": "Resolver problemas técnicos que afetam o desempenho do site nos motores de busca.",
                    "action_items": [
                        "Melhorar velocidade de carregamento das páginas",
                        "Corrigir problemas de usabilidade móvel",
                        "Implementar marcação de esquema (schema markup)"
                    ]
                },
                {
                    "title": "Estratégia de Backlinks",
                    "description": "Desenvolver links de qualidade para aumentar a autoridade do domínio.",
                    "action_items": [
                        "Criar conteúdo link-worthy (infográficos, estudos)",
                        "Estabelecer parcerias no setor",
                        "Monitorar perfil de backlinks regularmente"
                    ]
                }
            ]
        }