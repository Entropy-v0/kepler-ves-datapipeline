import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
import os
import sys
from dotenv import load_dotenv

# Forzar la carga del .env desde la raíz
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(root_path, ".env"))

if root_path not in sys.path:
    sys.path.append(root_path)

import config.settings as settings
from core.logger import get_logger

log = get_logger("SyncTool")

def get_db_engine():
    # 1. Aseguramos que el puerto sea un entero, si falla ponemos 5432
    try:
        port = int(os.getenv("DB_PORT", 5432))
    except (ValueError, TypeError):
        port = 5432

    # 2. Forzamos 127.0.0.1 para evitar el error del socket Unix
    host = "127.0.0.1"
    
    # 3. Obtenemos credenciales directamente de os.getenv para mayor seguridad
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASS", "kepler2004")
    db_name = os.getenv("DB_NAME", "kepler_db")

    conn_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
    
    log.info(f"Conectando a {host}:{port} (DB: {db_name})...")
    
    return create_engine(conn_url)

def sync_data():
    # ... (el resto de tu función sync_data permanece igual)
    csv_path = settings.RAW_FILE
    if not os.path.exists(csv_path):
        log.error(f"CSV no encontrado: {csv_path}")
        return

    log.info("--- Iniciando Sincronización ---")
    engine = get_db_engine()
    
    try:
        df_csv = pd.read_csv(csv_path)
        log.info("Verificando registros en la base de datos...")
        
        # Leemos la DB
        df_db = pd.read_sql("SELECT timestamp, merchant, price FROM p2p_ads", engine)
        
        # Comparar
        df_new = pd.merge(
            df_csv, df_db, 
            on=['timestamp', 'merchant', 'price'], 
            how='left', indicator=True
        ).query('_merge == "left_only"').drop(columns=['_merge'])

        if df_new.empty:
            log.info("Base de datos al día. Nada que importar.")
        else:
            log.info(f"Insertando {len(df_new)} registros nuevos...")
            df_new.to_sql('p2p_ads', engine, if_exists='append', index=False)
            log.info("¡Sincronización exitosa!")

    except Exception as e:
        if "does not exist" in str(e).lower():
            log.info("Creando tabla e importando historial completo...")
            df_csv.to_sql('p2p_ads', engine, if_exists='append', index=False)
            log.info("Importación inicial completada.")
        else:
            log.error(f"Error: {e}")

if __name__ == "__main__":
    sync_data()