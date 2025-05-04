# Jornada do Usuário: IA do Empreendedor

Este documento descreve a jornada completa do usuário na plataforma IA do Empreendedor, detalhando cada etapa da interação do usuário com o sistema.

## 📋 Índice

- [Visão Geral da Jornada](#visão-geral-da-jornada)
- [Fluxo Principal](#fluxo-principal)
- [Conexão de Carteira](#conexão-de-carteira)
- [Seleção de Relatório](#seleção-de-relatório)
- [Jornada de Geração de Relatório](#jornada-de-geração-de-relatório)
- [Exploração de Insights](#exploração-de-insights)
- [Download e Compartilhamento](#download-e-compartilhamento)
- [Pontos de Fricção e Soluções](#pontos-de-fricção-e-soluções)

## 🔍 Visão Geral da Jornada

A jornada do usuário na plataforma IA do Empreendedor é projetada para ser intuitiva, eficiente e valiosa, conduzindo empreendedores desde a autenticação até a obtenção de insights estratégicos personalizados.

```mermaid
graph LR
    A[Entrada na Plataforma] --> B[Conexão da Carteira]
    B --> C[Dashboard Principal]
    C --> D[Seleção de Relatório]
    D --> E[Preenchimento de Formulário]
    E --> F[Geração de Relatório]
    F --> G[Exploração de Insights]
    G --> H[Download/Compartilhamento]
    G --> D
    F --> D
```

## 🚶 Fluxo Principal

### 1. Acesso à Plataforma
O usuário acessa a plataforma IA do Empreendedor através de um navegador web.

### 2. Conexão de Carteira
O sistema solicita a conexão de uma carteira Web3 para autenticação do usuário.

### 3. Dashboard Principal
Após autenticação, o usuário é redirecionado para o dashboard principal.

### 4. Seleção de Relatório
O usuário escolhe o tipo de relatório que deseja gerar.

### 5. Preenchimento de Formulário
O sistema apresenta um formulário específico para o tipo de relatório escolhido.

### 6. Geração de Relatório
Após o preenchimento do formulário, o sistema gera o relatório solicitado.

### 7. Exploração de Insights
O usuário explora os insights, visualizações e recomendações do relatório.

### 8. Download e Compartilhamento
O usuário pode fazer download do relatório ou compartilhá-lo.

## 🔗 Conexão de Carteira

A conexão de carteira é o ponto de entrada principal para a plataforma:

```mermaid
sequenceDiagram
    participant User as Usuário
    participant LP as Landing Page
    participant WC as Wallet Connector
    participant W as Carteira Web3
    participant Dash as Dashboard

    User->>LP: Acessa plataforma
    LP->>User: Exibe opções de carteira
    User->>LP: Seleciona tipo de carteira
    LP->>WC: Solicita conexão
    WC->>W: Inicia solicitação
    alt Carteira instalada
        W->>User: Solicita aprovação
        User->>W: Confirma conexão
        W->>WC: Retorna endereço e assinatura
        WC->>LP: Confirma autenticação
    else Carteira não instalada
        W->>User: Prompt para instalar carteira
        User->>User: Instala carteira
        User->>LP: Reinicia processo
    end
    LP->>Dash: Redireciona para dashboard
    Dash->>User: Exibe dashboard personalizado
```

### Experiência do Usuário

- **Primeira Visita**: Para novos usuários, uma breve explicação sobre carteiras Web3 é fornecida.
- **Conexão Rápida**: Para usuários recorrentes, o sistema tenta reconectar automaticamente.
- **Modos de Fallback**: Opção para prosseguir sem conectar carteira em modo demo limitado.

## 📊 Seleção de Relatório

O processo de seleção de relatório é projetado para ser intuitivo:

```mermaid
flowchart TD
    A[Dashboard Principal] --> B{Escolha do Relatório}
    B -->|Business Map| C[Formulário de Business Map]
    B -->|Blue Ocean| D[Formulário de Blue Ocean]
    B -->|SEO| E[Formulário de SEO]
    C --> F[Preview do Relatório]
    D --> F
    E --> F
    F --> G{Confirmar Geração?}
    G -->|Sim| H[Processamento do Relatório]
    G -->|Não| B
    H --> I[Exibição do Relatório Completo]
```

### Diferenciação de Relatórios

Cada tipo de relatório é apresentado com:
- Descrição clara e objetiva
- Exemplo visual do resultado final
- Indicação do tempo estimado para geração
- Requisitos específicos de dados

## 📝 Jornada de Geração de Relatório

A geração de relatório é dividida em etapas lógicas com feedback constante ao usuário:

```mermaid
sequenceDiagram
    participant U as Usuário
    participant F as Formulário
    participant S as Sistema
    participant AI as IA
    participant R as Relatório

    U->>F: Preenche dados
    F->>U: Validação em tempo real
    U->>F: Finaliza preenchimento
    F->>S: Submete dados
    S->>U: Exibe progresso de processamento
    S->>AI: Envio de dados
    
    alt AI respondeu rapidamente
        AI->>S: Retorna análise
        S->>R: Gera relatório completo
    else AI demorando
        S->>U: Atualiza status de progresso
        AI->>S: Retorna análise
        S->>R: Gera relatório completo
    end
    
    R->>U: Exibe relatório interativo
```

### Formulários Inteligentes

Cada formulário inclui:
- Validação em tempo real
- Dicas contextuais
- Auto-preenchimento inteligente
- Salvamento automático de rascunhos

## 🔍 Exploração de Insights

A experiência de exploração do relatório é projetada para maximizar o valor para o usuário:

```mermaid
graph TD
    A[Relatório Gerado] --> B{Seções Interativas}
    B --> C[Resumo Executivo]
    B --> D[Análise Detalhada]
    B --> E[Visualizações]
    B --> F[Recomendações]
    
    C --> G[Navegação Contextual]
    D --> G
    E --> G
    F --> G
    
    G --> H{Ações do Usuário}
    H --> I[Aprofundar em Tópico]
    H --> J[Explorar Alternativas]
    H --> K[Filtrar Dados]
    
    I --> L[Nova Visualização]
    J --> L
    K --> L
    
    L --> M[Novos Insights]
    M --> H
```

### Funcionalidades Interativas

- **Gráficos Interativos**: Possibilidade de ajustar parâmetros e ver mudanças em tempo real
- **Drill-Down**: Aprofundamento em tópicos específicos
- **Filtros Dinâmicos**: Personalização da visualização de dados
- **Links Contextuais**: Navegação inteligente entre seções relacionadas

## 📤 Download e Compartilhamento

Múltiplas opções de exportação e compartilhamento:

```mermaid
flowchart LR
    A[Relatório Completo] --> B{Opções de Exportação}
    B --> C[PDF Completo]
    B --> D[Resumo Executivo]
    B --> E[Visualizações]
    B --> F[Dados Brutos CSV]
    
    A --> G{Compartilhamento}
    G --> H[Link Temporário]
    G --> I[Compartilhamento Direto]
    G --> J[Integração com Ferramentas]
```

### Formatos e Opções

- **PDF Personalizado**: Relatório completo com branding
- **Visualizações Individuais**: Exportação de gráficos específicos
- **Dados Estruturados**: Opção de exportar dados brutos para análise posterior
- **Compartilhamento Seguro**: Links temporários com controle de acesso

## 🚧 Pontos de Fricção e Soluções

A plataforma identifica potenciais desafios e implementa soluções proativas:

```mermaid
flowchart TD
    subgraph "Desafios Potenciais"
        A[Falha na API OpenAI]
        B[Carteira não Conectada]
        C[Dados Incompletos]
        D[Relatório Complexo]
    end
    
    subgraph "Soluções Implementadas"
        E[Mecanismo de Fallback]
        F[Modo Demo Limitado]
        G[Preenchimento Inteligente]
        H[Navegação Guiada]
    end
    
    A --> E
    B --> F
    C --> G
    D --> H
```

### Atendimento a Diversos Níveis de Usuários

- **Novos Usuários**: Experiência guiada com explicações contextuais
- **Usuários Intermediários**: Dicas avançadas opcionais
- **Usuários Avançados**: Opções de personalização profunda e exportação de dados