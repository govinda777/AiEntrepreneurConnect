#!/bin/bash

# Inicia a aplicação Streamlit em background
streamlit run main.py &
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