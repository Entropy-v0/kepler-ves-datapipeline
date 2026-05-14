import os
import pandas as pd
from sqlalchemy import create_engine
from core.logger import get_logger
import config.settings as settings

log = get_logger("Storage")

class DataStorage:
    def __init__(self):
        self.db_user = os.getenv('DB_USER')
        self.db_pass = os.getenv('DB_PASS')
        self.db_host = os.getenv('DB_HOST')
        self.db_port = os.getenv('DB_PORT', '5432')
        self.db_name = os.getenv('DB_NAME')
        
        self.csv_path = settings.RAW_FILE
        
        try:
            self.engine = create_engine(
                f'postgresql://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}'
            )
            log.info("Storage initialized: PostgreSQL connection engine ready.")
        except Exception as e:
            log.error(f"Failed to initialize DB engine: {e}")
            self.engine = None

    def save_to_csv(self, df):
        """Maneja la persistencia en el CSV para Kaggle."""
        try:
            exists = os.path.isfile(self.csv_path)
            df.to_csv(self.csv_path, mode='a', index=False, header=not exists)
            log.debug(f"Data appended to CSV: {self.csv_path}")
        except Exception as e:
            log.error(f"Error saving to CSV: {e}")

    def save_to_db(self, df):
        """Maneja la persistencia en PostgreSQL para ML/Streamlit."""
        if self.engine is None:
            log.warning("PostgreSQL engine not available. Skipping DB save.")
            return

        try:
            # 'if_exists=append' es clave para no borrar los datos anteriores
            df.to_sql('p2p_ads', self.engine, if_exists='append', index=False)
            log.debug("Data successfully pushed to PostgreSQL (table: p2p_ads).")
        except Exception as e:
            log.error(f"Error saving to PostgreSQL: {e}")

    def process_cycle_data(self, cycle_data):
        """
        Punto de entrada principal. Recibe la lista de diccionarios, 
        la convierte en DataFrame y la distribuye.
        """
        if not cycle_data:
            log.warning("No data received to save.")
            return

        df = pd.DataFrame(cycle_data)

        self.save_to_csv(df)
        self.save_to_db(df)
        
        log.info(f"Storage cycle complete: {len(cycle_data)} records secured.")