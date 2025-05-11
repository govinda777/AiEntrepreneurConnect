# Documentação da Camada Blockchain

## Visão Geral
Esta camada é responsável pela implementação da infraestrutura blockchain do AiEntrepreneurConnect, fornecendo uma base descentralizada e segura para as transações e interações entre empreendedores e investidores.

## Tecnologias Utilizadas
- Ethereum
- Solidity (Smart Contracts)
- Web3.js
- Truffle (Framework de desenvolvimento)
- OpenZeppelin (Contratos seguros e auditados)
- Ganache (Blockchain local para testes)

## Estrutura do Projeto
```
blockchain/
├── contracts/         # Smart contracts em Solidity
├── migrations/        # Scripts de migração
├── test/             # Testes dos smart contracts
└── truffle-config.js # Configuração do Truffle
```

## Smart Contracts Principais

### 1. ProjectRegistry
Responsável pelo registro e gerenciamento de projetos empreendedores na plataforma.

**Funcionalidades principais:**
- Registro de novos projetos
- Atualização de informações do projeto
- Listagem de projetos
- Gerenciamento de status do projeto

### 2. InvestmentContract
Gerencia as transações de investimento entre investidores e empreendedores.

**Funcionalidades principais:**
- Processamento de investimentos
- Registro de transações
- Distribuição de tokens
- Gestão de retornos financeiros

### 3. UserRegistry
Controla o registro e autenticação de usuários na plataforma.

**Funcionalidades principais:**
- Registro de usuários
- Verificação de identidade
- Gerenciamento de perfis
- Controle de permissões

## Como Utilizar

### Pré-requisitos
- Node.js (v14 ou superior)
- NPM ou Yarn
- MetaMask ou carteira Web3 compatível

### Configuração do Ambiente
1. Instale as dependências:
```bash
npm install --registry https://registry.npmjs.org/
```

Se encontrar problemas durante a instalação, tente os seguintes passos:

```bash
# Limpar o cache do npm
npm cache clean --force

# Remover node_modules e package-lock.json
rm -rf node_modules package-lock.json

# Reinstalar as dependências usando o registro público
npm install --registry https://registry.npmjs.org/
```

2. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

3. Compile os contratos:
```bash
npm run compile
```

### Deploy dos Contratos
1. Para deploy na rede de teste:
```bash
npm run migrate -- --network development
```

2. Para deploy na mainnet:
```bash
npm run migrate -- --network mainnet
```

## Testes
Execute os testes automatizados:
```bash
npm test
```

## Segurança
- Todos os contratos passam por auditorias de segurança
- Implementação de padrões OpenZeppelin
- Mecanismos de pausa para emergências
- Controles de acesso baseados em roles

## Integração com Frontend
A integração com o frontend é feita através da biblioteca Web3.js. Exemplo de conexão:

```javascript
const Web3 = require('web3');
const web3 = new Web3(window.ethereum);

// Conectar carteira
await window.ethereum.enable();

// Interagir com contratos
const contract = new web3.eth.Contract(ABI, CONTRACT_ADDRESS);
```

## Manutenção e Atualizações
- Monitoramento constante da rede
- Atualizações de segurança regulares
- Implementação de upgrades através de padrões proxy
- Backup e recuperação de dados

## Contribuição
Para contribuir com o desenvolvimento:
1. Faça fork do repositório
2. Crie uma branch para sua feature
3. Faça commit das alterações
4. Envie um pull request

## Suporte
Para suporte técnico ou dúvidas:
- Abra uma issue no repositório
- Entre em contato com a equipe de desenvolvimento

## Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Como Executar os Testes

### Pré-requisitos
- Node.js (v14 ou superior)
- NPM ou Yarn
- Ganache (blockchain local para testes)

### Configuração do Ambiente

1. Instale as dependências:
```bash
npm install
```

2. Inicie o Ganache:
- Você pode usar a interface gráfica do Ganache ou executar via linha de comando:
```bash
npx ganache-cli
```

3. Execute os testes:
```bash
npm test
```

### Descrição dos Testes

O sistema de testes verifica as seguintes funcionalidades:

1. **Inicialização do Contrato**
   - Configuração correta do owner
   - Configuração correta do token da plataforma
   - Verificação do custo do relatório

2. **Solicitação de Relatório**
   - Solicitação bem-sucedida
   - Falha por saldo insuficiente
   - Falha por allowance insuficiente

3. **Definição do Hash do Relatório**
   - Definição bem-sucedida pelo owner
   - Falha por usuário não autorizado
   - Falha por prazo expirado

4. **Reembolso de Relatório**
   - Reembolso bem-sucedido após prazo
   - Falha por relatório já gerado
   - Falha por prazo não atingido

5. **Extensão de Prazo**
   - Extensão bem-sucedida pelo owner
   - Falha por usuário não autorizado

6. **Retirada de Tokens**
   - Retirada bem-sucedida pelo owner
   - Falha por usuário não autorizado

7. **Consultas de Relatórios**
   - Listagem de relatórios do usuário
   - Detalhes do relatório
   - Falha por acesso não autorizado

## Cobertura de Testes

Os testes cobrem:
- Fluxos de sucesso
- Condições de erro
- Verificações de permissão
- Eventos emitidos
- Estados do contrato
- Manipulação de tokens

## Desenvolvimento

Para adicionar novos testes:

1. Crie um novo arquivo de teste em `test/`
2. Siga o padrão de organização existente:
   - Descrição do grupo de testes
   - Setup necessário (beforeEach)
   - Casos de teste individuais
   - Verificações de eventos e estados

3. Execute os testes para garantir que não há regressões:
```bash
npm test
```
