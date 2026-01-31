from openai import OpenAI
from dotenv import load_dotenv
import os
import json 
import re

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
    
    # Estrae il contenuto della risposta
    content = response.choices[0].message.content
    
    # Pulizia del contenuto per gestire formattazioni extra
    # Rimuovi eventuali code blocks markdown
    content = re.sub(r'```json\s*', '', content)
    content = re.sub(r'```\s*', '', content)
    
    # Rimuovi spazi bianchi extra all'inizio e alla fine
    content = content.strip()
    
    try:
        result = json.loads(content)
        print(f"[DEBUG] Risposta AI parsata: {result}")
        return result
    except json.JSONDecodeError as e:
        print(f"[ERROR] Errore nel parsing JSON: {e}")
        print(f"[ERROR] Contenuto ricevuto: {content[:500]}")
        raise ValueError(f"L'AI ha restituito un JSON non valido: {e}")