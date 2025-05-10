# Estrutura de Relatórios

Este diretório contém a implementação da estrutura de geração de relatórios, que é dividida em três componentes principais:

## 1. Templates (`/templates`)

Os templates são responsáveis por definir a estrutura e formatação dos relatórios. Eles:
- Definem o formato de saída do relatório
- Garantem consistência na apresentação
- Formatam os dados para exibição
- Gerenciam seções e componentes visuais

### Estrutura Base
- `base_template.py`: Define a interface base para todos os templates
- Templates específicos herdam desta base e implementam a formatação para cada tipo de relatório

## 2. Prompts (`/prompts`)

Os prompts são responsáveis por definir as instruções para o LLM. Eles:
- Definem o comportamento do modelo
- Estruturam as perguntas e análises
- Garantem consistência nas respostas
- Mantêm o contexto entre diferentes partes da análise

### Estrutura Base
- `base_prompt.py`: Define a interface base para todos os prompts
- Cada tipo de relatório tem seu próprio conjunto de prompts específicos

## 3. LLM Configs (`/llm_configs`)

As configurações de LLM gerenciam a interação com os modelos de linguagem. Elas:
- Definem parâmetros do modelo
- Gerenciam a geração de conteúdo
- Validam as saídas
- Tratam erros e exceções

### Estrutura Base
- `base_llm.py`: Define a interface base para configurações de LLM
- Cada tipo de relatório pode ter sua própria configuração específica de LLM

## Uso

Para criar um novo tipo de relatório:

1. Crie um novo template herdando de `ReportTemplate`
2. Crie um novo conjunto de prompts herdando de `ReportPrompt`
3. Crie uma nova configuração de LLM herdando de `ReportLLM`
4. Implemente as funções necessárias em cada componente

### Exemplo de Uso

```python
from templates.business_map_template import BusinessMapTemplate
from prompts.business_map_prompt import BusinessMapPrompt
from llm_configs.business_map_llm import BusinessMapLLM

# Criar instâncias
template = BusinessMapTemplate(report_id, generated_date)
prompt = BusinessMapPrompt()
llm = BusinessMapLLM()

# Gerar relatório
prompts = prompt.get_prompts(data)
analysis = llm.generate_analysis(prompts, data)
recommendations = llm.generate_recommendations(prompts, analysis)

# Combinar e validar dados
report_data = {**data, **analysis, 'recommendations': recommendations}
if llm.validate_output(report_data):
    report = template.generate(report_data)
```

## Boas Práticas

1. **Separação de Responsabilidades**
   - Templates cuidam APENAS da formatação
   - Prompts cuidam APENAS das instruções
   - LLM configs cuidam APENAS da interação com o modelo

2. **Validação**
   - Sempre valide as saídas do LLM
   - Garanta que os dados estão no formato esperado
   - Trate erros apropriadamente

3. **Manutenção**
   - Mantenha os prompts atualizados
   - Documente mudanças nos templates
   - Monitore o desempenho dos LLMs

4. **Extensibilidade**
   - Mantenha as interfaces base consistentes
   - Permita personalização quando necessário
   - Facilite a adição de novos tipos de relatório 