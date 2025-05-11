#!/bin/bash

# Verifica se o arquivo .env existe
if [ ! -f .env ]; then
    echo "Erro: Arquivo .env não encontrado."
    echo "Por favor, crie um arquivo .env baseado no env.example com suas configurações."
    exit 1
fi

# Carrega as variáveis do arquivo .env
set -a
source .env
set +a

# Verifica se a variável OPENAI_API_KEY está definida
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Erro: A variável OPENAI_API_KEY não está definida no arquivo .env."
    echo "Por favor, adicione OPENAI_API_KEY ao seu arquivo .env."
    exit 1
fi

# Define a porta padrão se não estiver definida
STREAMLIT_PORT=${STREAMLIT_PORT:-5001}

# Função para verificar se o servidor está rodando
check_server() {
    for i in {1..60}; do
        if curl -s "http://localhost:${STREAMLIT_PORT}/_stcore/health" > /dev/null; then
            echo "Servidor Streamlit está rodando na porta ${STREAMLIT_PORT}"
            # Aguarda mais 5 segundos para garantir que a aplicação está totalmente carregada
            sleep 5
            return 0
        fi
        echo "Aguardando servidor iniciar... (tentativa $i/60)"
        sleep 2
    done
    echo "Erro: Servidor não iniciou após 120 segundos"
    return 1
}

# Inicia a aplicação Streamlit em background
echo "Iniciando servidor Streamlit na porta ${STREAMLIT_PORT}..."
streamlit run main.py --server.port $STREAMLIT_PORT --server.headless true &
STREAMLIT_PID=$!

# Aguarda o servidor iniciar
if ! check_server; then
    kill $STREAMLIT_PID
    exit 1
fi

# Roda os testes
echo "Rodando testes e2e..."
pytest tests/e2e
TEST_RESULT=$?

# Mata o processo da aplicação
kill $STREAMLIT_PID

# Retorna o código de saída dos testes
exit $TEST_RESULT 