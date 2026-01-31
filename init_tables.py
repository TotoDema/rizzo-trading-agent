"""
Script di debug per verificare e creare le tabelle
"""
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.getenv("DATABASE_URL")
print(f"🔍 DATABASE_URL: {db_url}")

if not db_url:
    print("❌ DATABASE_URL non trovata!")
    exit(1)

try:
    # Connessione diretta
    print("\n🔌 Connessione al database...")
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    # Verifica tabelle esistenti
    print("\n📋 Tabelle esistenti nel database:")
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    tables = cur.fetchall()
    
    if tables:
        for table in tables:
            print(f"  ✓ {table[0]}")
    else:
        print("  ⚠️  Nessuna tabella trovata!")
    
    # Ora creiamo le tabelle usando lo schema da db_utils
    print("\n🏗️  Creazione tabelle...")
    
    # Schema SQL completo
    schema_sql = """
    CREATE TABLE IF NOT EXISTS account_snapshots (
        id              BIGSERIAL PRIMARY KEY,
        created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        balance_usd     NUMERIC(20, 8) NOT NULL,
        raw_payload     JSONB NOT NULL
    );

    CREATE TABLE IF NOT EXISTS open_positions (
        id                  BIGSERIAL PRIMARY KEY,
        snapshot_id         BIGINT NOT NULL REFERENCES account_snapshots(id) ON DELETE CASCADE,
        symbol              TEXT NOT NULL,
        side                TEXT NOT NULL,
        size                NUMERIC(30, 10) NOT NULL,
        entry_price         NUMERIC(30, 10),
        mark_price          NUMERIC(30, 10),
        pnl_usd             NUMERIC(30, 10),
        leverage            TEXT,
        raw_payload         JSONB NOT NULL
    );

    CREATE INDEX IF NOT EXISTS idx_open_positions_snapshot_id
        ON open_positions(snapshot_id);

    CREATE TABLE IF NOT EXISTS ai_contexts (
        id              BIGSERIAL PRIMARY KEY,
        created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        system_prompt   TEXT
    );

    CREATE TABLE IF NOT EXISTS indicators_contexts (
        id                      BIGSERIAL PRIMARY KEY,
        context_id              BIGINT NOT NULL REFERENCES ai_contexts(id) ON DELETE CASCADE,
        ticker                  TEXT NOT NULL,
        ts                      TIMESTAMPTZ,
        price                   NUMERIC(20, 8),
        ema20                   NUMERIC(20, 8),
        macd                    NUMERIC(20, 8),
        rsi_7                   NUMERIC(20, 8),
        volume_bid              NUMERIC(20, 8),
        volume_ask              NUMERIC(20, 8),
        pp                      NUMERIC(20, 8),
        s1                      NUMERIC(20, 8),
        s2                      NUMERIC(20, 8),
        r1                      NUMERIC(20, 8),
        r2                      NUMERIC(20, 8),
        open_interest_latest    NUMERIC(30, 10),
        open_interest_average   NUMERIC(30, 10),
        funding_rate            NUMERIC(20, 8),
        ema20_15m               NUMERIC(20, 8),
        ema50_15m               NUMERIC(20, 8),
        atr3_15m                NUMERIC(20, 8),
        atr14_15m               NUMERIC(20, 8),
        volume_15m_current      NUMERIC(30, 10),
        volume_15m_average      NUMERIC(30, 10),
        intraday_mid_prices     JSONB,
        intraday_ema20_series   JSONB,
        intraday_macd_series    JSONB,
        intraday_rsi7_series    JSONB,
        intraday_rsi14_series   JSONB,
        lt15m_macd_series       JSONB,
        lt15m_rsi14_series      JSONB
    );

    CREATE TABLE IF NOT EXISTS news_contexts (
        id              BIGSERIAL PRIMARY KEY,
        context_id      BIGINT NOT NULL REFERENCES ai_contexts(id) ON DELETE CASCADE,
        news_text       TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS sentiment_contexts (
        id                      BIGSERIAL PRIMARY KEY,
        context_id              BIGINT NOT NULL REFERENCES ai_contexts(id) ON DELETE CASCADE,
        value                   INTEGER,
        classification          TEXT,
        sentiment_timestamp     BIGINT,
        raw                     JSONB
    );

    CREATE TABLE IF NOT EXISTS forecasts_contexts (
        id                      BIGSERIAL PRIMARY KEY,
        context_id              BIGINT NOT NULL REFERENCES ai_contexts(id) ON DELETE CASCADE,
        ticker                  TEXT NOT NULL,
        timeframe               TEXT NOT NULL,
        last_price              NUMERIC(30, 10),
        prediction              NUMERIC(30, 10),
        lower_bound             NUMERIC(30, 10),
        upper_bound             NUMERIC(30, 10),
        change_pct              NUMERIC(10, 4),
        forecast_timestamp      BIGINT,
        raw                     JSONB
    );

    CREATE TABLE IF NOT EXISTS bot_operations (
        id                  BIGSERIAL PRIMARY KEY,
        created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        context_id          BIGINT REFERENCES ai_contexts(id) ON DELETE CASCADE,
        operation           TEXT NOT NULL,
        symbol              TEXT,
        direction           TEXT,
        target_portion_of_balance NUMERIC(10, 4),
        leverage            NUMERIC(10, 4),
        raw_payload         JSONB NOT NULL
    );

    CREATE INDEX IF NOT EXISTS idx_bot_operations_created_at
        ON bot_operations(created_at);

    CREATE TABLE IF NOT EXISTS errors (
        id              BIGSERIAL PRIMARY KEY,
        created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        error_type      TEXT NOT NULL,
        error_message   TEXT,
        traceback       TEXT,
        context         JSONB,
        source          TEXT
    );

    CREATE INDEX IF NOT EXISTS idx_errors_created_at
        ON errors(created_at);
    """
    
    # Esegui lo schema
    cur.execute(schema_sql)
    conn.commit()
    
    print("✅ Schema eseguito!")
    
    # Verifica di nuovo le tabelle
    print("\n📋 Tabelle dopo la creazione:")
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    tables = cur.fetchall()
    
    for table in tables:
        print(f"  ✓ {table[0]}")
    
    print(f"\n✅ Totale tabelle create: {len(tables)}")
    
    cur.close()
    conn.close()
    
    print("\n🎉 Setup completato con successo!")
    
except Exception as e:
    print(f"\n❌ Errore: {e}")
    import traceback
    traceback.print_exc()
