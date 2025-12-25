from sqlalchemy import create_engine, text
import pandas as pd

# --- Konfigurasi koneksi ---
DB_USER = "root"
DB_PASS = "cCoiaAEpiqVgAaqcAyjdxORwIDyKWGZw"
DB_HOST = "tramway.proxy.rlwy.net"
DB_PORT = "27684"
DB_NAME = "railway"

engine = create_engine(
    f"mysql://root:cCoiaAEpiqVgAaqcAyjdxORwIDyKWGZw@tramway.proxy.rlwy.net:27684/railway",
    pool_pre_ping=True
)

def fetch_data(query, params=None):
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn, params=params)

def execute_query(query, params=None):
    with engine.begin() as conn:
        conn.execute(text(query), params or {})

def get_engine():
    return engine
