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

# Inicia a aplicação Streamlit em background
streamlit run main.py --server.port $STREAMLIT_PORT &
STREAMLIT_PID=$!

# Aguarda a aplicação iniciar
sleep 5

# Roda os testes
echo "Rodando testes e2e..."
pytest tests/e2e
TEST_RESULT=$?

# Mata o processo da aplicação
kill $STREAMLIT_PID

# Retorna o código de saída dos testes
exit $TEST_RESULT 