"""
Script per visualizzare gli errori salvati nel database
"""
import psycopg2
from dotenv import load_dotenv
import os
import json
import sys

load_dotenv()

# Redirect to file
output = open('errors_output.txt', 'w', encoding='utf-8')
sys.stdout = output
sys.stderr = output

try:
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()
    
    # Prendi gli ultimi 5 errori
    cur.execute("""
        SELECT id, created_at, error_type, error_message, traceback, context, source
        FROM errors
        ORDER BY created_at DESC
        LIMIT 5;
    """)
    
    errors = cur.fetchall()
    
    print("=" * 80)
    print("ULTIMI ERRORI NEL DATABASE")
    print("=" * 80)
    
    if not errors:
        print("\n✅ Nessun errore trovato!")
    else:
        for i, (id, created_at, error_type, error_message, traceback, context, source) in enumerate(errors, 1):
            print(f"\n{'='*80}")
            print(f"ERRORE #{id} - {created_at}")
            print(f"{'='*80}")
            print(f"Tipo: {error_type}")
            print(f"Source: {source}")
            print(f"Messaggio: {error_message}")
            print(f"\nTraceback:")
            print(traceback)
            
            if context:
                print(f"\nContext:")
                # Mostra solo le chiavi principali del context per non sovraccaricare
                if isinstance(context, dict):
                    for key in ['prompt', 'tickers', 'balance']:
                        if key in context and context[key]:
                            if key == 'prompt':
                                print(f"  {key}: {str(context[key])[:200]}...")
                            else:
                                print(f"  {key}: {context[key]}")
            print()
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Errore nella lettura del database: {e}")
    import traceback
    traceback.print_exc()

output.close()
print("Output salvato in errors_output.txt", file=sys.__stdout__)
