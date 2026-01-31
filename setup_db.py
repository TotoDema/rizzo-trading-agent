import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()

# Configurazione
DB_NAME = "trading_db"
DB_USER = "TradingAgentUser"
DB_PASSWORD = "trading123"  # Cambia se vuoi
DB_HOST = "localhost"
DB_PORT = "5432"

# Connessione al database postgres di default per creare il nuovo database
postgres_url = os.getenv("DATABASE_URL")
if not postgres_url:
    print("❌ DATABASE_URL non trovata nel file .env")
    print("Aggiungi questa riga al file .env:")
    print("DATABASE_URL=postgresql://postgres:TUA_PASSWORD@localhost:5432/postgres")
    exit(1)

try:
    # Connessione al database postgres
    print("🔌 Connessione a PostgreSQL...")
    conn = psycopg2.connect(postgres_url)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    
    # Crea l'utente se non esiste
    print(f"👤 Creazione utente {DB_USER}...")
    try:
        cur.execute(f"""
            CREATE USER {DB_USER} WITH PASSWORD '{DB_PASSWORD}';
        """)
        print(f"✅ Utente {DB_USER} creato")
    except psycopg2.errors.DuplicateObject:
        print(f"ℹ️  Utente {DB_USER} già esistente")
    
    # Crea il database se non esiste
    print(f"🗄️  Creazione database {DB_NAME}...")
    try:
        cur.execute(f"""
            CREATE DATABASE {DB_NAME} OWNER {DB_USER};
        """)
        print(f"✅ Database {DB_NAME} creato")
    except psycopg2.errors.DuplicateDatabase:
        print(f"ℹ️  Database {DB_NAME} già esistente")
    
    # Dai i permessi
    print(f"🔐 Assegnazione permessi...")
    cur.execute(f"""
        GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {DB_USER};
    """)
    print(f"✅ Permessi assegnati")
    
    cur.close()
    conn.close()
    
    # Ora connettiti al nuovo database e crea le tabelle
    print(f"\n📊 Creazione tabelle nel database {DB_NAME}...")
    new_db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # Aggiorna temporaneamente la variabile d'ambiente
    os.environ["DATABASE_URL"] = new_db_url
    
    # Importa e usa la funzione init_db dal tuo db_utils
    import db_utils
    db_utils.init_db()
    
    print("\n✅ Setup completato con successo!")
    print(f"\n📝 Aggiungi questa riga al tuo file .env:")
    print(f"DATABASE_URL={new_db_url}")
    
except Exception as e:
    print(f"\n❌ Errore: {e}")
    print(f"\nDettagli: {type(e).__name__}")
