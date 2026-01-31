"""
Script di test per verificare la risposta dell'AI - con output su file
"""
from trading_agent import previsione_trading_agent
import json
import sys

# Redirect output to file
output_file = open('test_output.txt', 'w', encoding='utf-8')
sys.stdout = output_file
sys.stderr = output_file

# Test con un prompt semplice
test_prompt = """
You are a cryptocurrency trading AI. Respond with ONLY a JSON object.

REQUIRED JSON FORMAT (ALL fields are MANDATORY):
{
  "operation": "open" | "close" | "hold",
  "symbol": "BTC" | "ETH" | "SOL",
  "direction": "long" | "short",
  "target_portion_of_balance": 0.0-1.0,
  "leverage": 1-10,
  "reason": "your explanation here"
}

Portfolio: Balance $1000, no open positions.
Market: BTC is trending up.

Decide what to do.
"""

print("=" * 60)
print("TEST RISPOSTA AI")
print("=" * 60)

try:
    result = previsione_trading_agent(test_prompt)
    print("\n✅ JSON parsato con successo!")
    print(f"\nRisultato:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Verifica campi richiesti
    required = ["operation", "symbol", "direction", "target_portion_of_balance", "leverage", "reason"]
    missing = [f for f in required if f not in result]
    
    if missing:
        print(f"\n⚠️  Campi mancanti: {missing}")
    else:
        print("\n✅ Tutti i campi richiesti sono presenti!")
        
except Exception as e:
    print(f"\n❌ Errore: {e}")
    import traceback
    traceback.print_exc()

output_file.close()
print("Output salvato in test_output.txt", file=sys.__stdout__)
