from trading_agent import previsione_trading_agent
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Test prompt mimicking the real one
test_prompt = """
Analizza i seguenti dati e decidi l'operazione di trading.
<indicatori>
BTC: RSI=45, MACD=Slightly Bearish
</indicatori>
<news>
Nessuna news importante.
</news>
Torna un JSON con: operation (open/close/hold), symbol (BTC), direction (long/short), target_portion_of_balance (0-1), leverage (1-10), reason (string).
"""

print("--- Test OpenRouter Connection ---")
if not os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY") == "tuo_api_key_qui":
    print("❌ Errore: Inserisci la tua OPENROUTER_API_KEY nel file .env prima di testare!")
else:
    try:
        result = previsione_trading_agent(test_prompt)
        print("✅ Successo! Risposta ricevuta:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"❌ Errore durante la chiamata: {e}")
