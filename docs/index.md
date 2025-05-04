# Documentação: IA do Empreendedor

Bem-vindo à documentação da plataforma IA do Empreendedor. Este conjunto de documentos fornece informações detalhadas sobre a arquitetura, funcionamento e uso do sistema.

## 📋 Índice Geral

### [README Principal](../README.md)
Visão geral do projeto, requisitos e instruções de instalação.

### [Visão Técnica](technical_overview.md)
Detalhamento da arquitetura, fluxo de dados e componentes do sistema.

```mermaid
graph TD
    A[Documentação] --> B[Visão Geral]
    A --> C[Documentação Técnica]
    A --> D[Guias de Usuário]
    A --> E[Testes]
    
    B --> B1[README.md]
    
    C --> C1[technical_overview.md]
    
    D --> D1[user_journey.md]
    
    E --> E1[e2e_testing.md]
```

## 📚 Estrutura da Documentação

### Documentação de Arquitetura
- [Visão Técnica](technical_overview.md): Arquitetura completa do sistema, módulos e integração com OpenAI

### Documentação de Usuário
- [Jornada do Usuário](user_journey.md): Descrição detalhada da experiência do usuário na plataforma

### Testes e Qualidade
- [Plano de Testes E2E](e2e_testing.md): Plano completo de testes end-to-end para a plataforma

## 📊 Diagramas Principais

### Arquitetura do Sistema

```mermaid
flowchart TD
    subgraph Interface[Interface do Usuário]
        main[main.py]
        dashboard[dashboard.py]
        forms[forms.py]
    end
    
    subgraph Backend[Lógica de Negócios]
        report_gen[report_generator.py]
        api_client[api_client.py]
        openai_client[openai_client.py]
        visualization[visualization.py]
    end
    
    subgraph Utilitários[Utilitários e Conectores]
        utils[utils.py]
        wallet[wallet_connector.py]
    end
    
    main --> dashboard
    main --> forms
    forms --> api_client
    dashboard --> report_gen
    api_client --> openai_client
    report_gen --> visualization
    wallet --> main
    api_client --> report_gen
    main --> utils
    report_gen --> utils
    openai_client --> utils
```

### Fluxo de Usuário Simplificado

```mermaid
graph LR
    A[Entrada na Plataforma] --> B[Conexão da Carteira]
    B --> C[Dashboard Principal]
    C --> D[Seleção de Relatório]
    D --> E[Preenchimento de Formulário]
    E --> F[Geração de Relatório]
    F --> G[Exploração de Insights]
```

### Processo de Integração com OpenAI

```mermaid
sequenceDiagram
    participant U as Usuário
    participant App as Aplicação
    participant OAI as OpenAI Client
    participant API as OpenAI API
    participant R as Report Generator

    U->>App: Submete formulário
    App->>OAI: Solicita análise
    
    alt API disponível
        OAI->>API: Envia prompt com template
        API->>OAI: Retorna análise JSON
        OAI->>R: Envia dados estruturados
    else API indisponível
        OAI->>OAI: Detecta indisponibilidade
        OAI->>OAI: Gera dados simulados
        OAI->>R: Envia dados simulados
    end
    
    R->>App: Gera relatório
    App->>U: Exibe relatório
```

## 🔄 Atualização da Documentação

Estas documentações devem ser mantidas atualizadas conforme o projeto evolui. Ao fazer mudanças no código:

1. Verifique se a alteração impacta algum diagrama ou descrição
2. Atualize os diagramas Mermaid conforme necessário
3. Revise as descrições de fluxo e comportamento
4. Atualize os casos de teste quando novas funcionalidades forem adicionadas