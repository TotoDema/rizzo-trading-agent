"""
Verifica rapida delle tabelle create
"""
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

try:
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()
    
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    
    tables = cur.fetchall()
    
    print("=" * 50)
    print("TABELLE NEL DATABASE Trading_Agent")
    print("=" * 50)
    
    if not tables:
        print("⚠️  NESSUNA TABELLA TROVATA!")
    else:
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table[0]}")
        print(f"\n✅ Totale: {len(tables)} tabelle")
    
    print("=" * 50)
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Errore: {e}")
