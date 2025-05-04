# Plano de Testes End-to-End (E2E)

## Visão Geral
Este documento descreve o plano de testes end-to-end para a aplicação "IA do Empreendedor", uma aplicação Streamlit que permite usuários conectarem suas carteiras digitais e gerarem relatórios personalizados.

## Ferramentas Recomendadas
- **Playwright**: Framework de automação de testes moderno e robusto
- **Pytest**: Para estruturação e execução dos testes
- **Pytest-playwright**: Plugin para integração do Playwright com Pytest

## Cenários de Teste

### 1. Autenticação
- **Cenário**: Conectar com Metamask
  - Dado que o usuário está na página inicial
  - Quando o usuário clica no botão "Conectar Metamask"
  - Então o usuário deve ser autenticado
  - E o endereço da carteira deve ser exibido
  - E o saldo de tokens deve ser exibido

- **Cenário**: Conectar com WalletConnect
  - Dado que o usuário está na página inicial
  - Quando o usuário clica no botão "Conectar WalletConnect"
  - Então o usuário deve ser autenticado
  - E o endereço da carteira deve ser exibido
  - E o saldo de tokens deve ser exibido

### 2. Seleção de Relatório
- **Cenário**: Visualizar tipos de relatório disponíveis
  - Dado que o usuário está autenticado
  - Quando o usuário acessa o dashboard
  - Então todos os tipos de relatório devem ser exibidos
  - E o custo em tokens deve ser visível para cada relatório

- **Cenário**: Selecionar um relatório
  - Dado que o usuário está autenticado
  - Quando o usuário seleciona um tipo de relatório
  - Então o formulário correspondente deve ser exibido

### 3. Preenchimento de Formulário
- **Cenário**: Preencher formulário válido
  - Dado que o usuário selecionou um relatório
  - Quando o usuário preenche todos os campos obrigatórios
  - E clica em "Gerar Relatório"
  - Então o processamento deve iniciar
  - E o relatório deve ser gerado com sucesso

- **Cenário**: Tentar gerar relatório com formulário incompleto
  - Dado que o usuário selecionou um relatório
  - Quando o usuário deixa campos obrigatórios em branco
  - E clica em "Gerar Relatório"
  - Então uma mensagem de erro deve ser exibida

### 4. Visualização de Relatório
- **Cenário**: Visualizar relatório gerado
  - Dado que um relatório foi gerado com sucesso
  - Quando o usuário acessa o dashboard
  - Então o relatório deve aparecer na lista de relatórios recentes
  - E o usuário deve poder visualizar os detalhes do relatório

### 5. Gestão de Tokens
- **Cenário**: Verificar saldo de tokens
  - Dado que o usuário está autenticado
  - Quando o usuário acessa o dashboard
  - Então o saldo atual de tokens deve ser exibido corretamente

- **Cenário**: Consumo de tokens ao gerar relatório
  - Dado que o usuário tem tokens suficientes
  - Quando o usuário gera um relatório
  - Então o custo do relatório deve ser debitado do saldo

## Estrutura do Projeto de Testes
```
tests/
├── e2e/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_authentication.py
│   ├── test_report_selection.py
│   ├── test_form_submission.py
│   ├── test_report_viewing.py
│   └── test_token_management.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
└── config/
    ├── __init__.py
    └── test_config.py
```

## Configuração Inicial
1. Instalar dependências:
```bash
pip install pytest playwright pytest-playwright
playwright install
```

2. Configurar ambiente de teste:
- Criar arquivo de configuração com URLs e credenciais
- Configurar variáveis de ambiente para diferentes ambientes (dev, staging, prod)

## Execução dos Testes
```bash
# Executar todos os testes
pytest tests/e2e/

# Executar testes específicos
pytest tests/e2e/test_authentication.py

# Executar com relatório detalhado
pytest tests/e2e/ --html=report.html
```

## Próximos Passos
1. Implementar a estrutura básica do projeto de testes
2. Configurar o ambiente de CI/CD para execução automática dos testes
3. Implementar os testes gradualmente, começando pelos cenários críticos
4. Adicionar testes de integração com serviços externos
5. Implementar relatórios de cobertura de testes
