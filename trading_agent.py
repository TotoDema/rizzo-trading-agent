from openai import OpenAI
from dotenv import load_dotenv
import os
import json 

load_dotenv()
# read api key
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
# Inizializza il client per OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def previsione_trading_agent(prompt):
    # Esempio di modello su OpenRouter (puoi cambiarlo con quello che preferisci)
    # Es: "deepseek/deepseek-chat", "openai/gpt-4o-mini", "anthropic/claude-3-haiku"
    model_name = "openai/gpt-4o-mini" 

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": prompt}
        ],
        response_format={ "type": "json_object" }
    )
    
    # Estrae il contenuto della risposta e lo converte in JSON
    content = response.choices[0].message.content
    return json.loads(content)