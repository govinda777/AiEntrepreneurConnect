import openai
import os
import re
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def test_prompt(client):
    try:
        model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
        print(f"\n🔎 Testando envio de prompt para o modelo {model}...")
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Diga 'Olá, mundo!'"}],
            max_tokens=10
        )
        reply = response.choices[0].message.content.strip()
        print(f"Resposta do modelo: {reply}")
        print("\n✅ Você está apto a enviar prompts para a aplicação!")
    except Exception as e:
        print(f"❌ Erro ao enviar prompt: {str(e)}")

def check_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Check if API key exists
    if not api_key:
        print("❌ API key não encontrada. Configure a variável de ambiente OPENAI_API_KEY.")
        return False

    print(f"\n🔑 Usando API key: {api_key[:4]}...{api_key[-4:] if len(api_key) > 8 else ''}")
    client = openai.OpenAI(api_key=api_key)
    
    try:
        # Check if API key is valid and has permissions
        models = client.models.list()
        print("✅ Chave válida e com permissões corretas.")
        print("\nModelos disponíveis:")
        for model in models.data:
            print("-", model.id)
        
        # Check remaining quota by making a simple completion request
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            print("\n✅ Quota disponível e funcionando corretamente.")
        except openai.RateLimitError:
            print("\n⚠️ Aviso: Quota excedida ou limite de requisições atingido.")
        except Exception as e:
            print(f"\n⚠️ Aviso: Erro ao verificar quota: {str(e)}")
        
        # Testar envio de prompt
        test_prompt(client)
        return True
        
    except openai.AuthenticationError:
        print("❌ Chave inválida ou sem permissões.")
        return False
    except Exception as e:
        print(f"❌ Erro ao verificar a API key: {str(e)}")
        print(f"Tipo do erro: {type(e).__name__}")
        if hasattr(e, 'response'):
            print(f"Status code: {e.response.status_code if hasattr(e.response, 'status_code') else 'N/A'}")
            print(f"Response: {e.response.text if hasattr(e.response, 'text') else 'N/A'}")
        return False

if __name__ == "__main__":
    check_api_key()