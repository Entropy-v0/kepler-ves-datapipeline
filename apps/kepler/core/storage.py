import os
import pandas as pd
from sqlalchemy import create_engine
from core.logger import get_logger
import config.settings as settings

log = get_logger("Storage")

class DataStorage:
    def __init__(self):
        from sqlalchemy.engine import URL
        
        self.csv_path = settings.RAW_FILE
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)
        
        try:
            url_object = URL.create(
                "postgresql",
                username=settings.DB_USER,
                password=settings.DB_PASS,
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                database=settings.DB_NAME,
            )
            self.engine = create_engine(url_object)
            log.info("Storage initialized: PostgreSQL connection engine ready.")
        except Exception as e:
            log.error(f"Failed to initialize DB engine: {e}")
            self.engine = None

    def save_to_csv(self, df):
        """Handles persistence to CSV for local analysis."""
        try:
            exists = os.path.isfile(self.csv_path)
            df.to_csv(self.csv_path, mode='a', index=False, header=not exists)
            log.debug(f"Data appended to CSV: {self.csv_path}")
        except Exception as e:
            log.error(f"Error saving to CSV: {e}")

    def save_to_db(self, df):
        """Handles persistence to PostgreSQL for ML/Streamlit applications."""
        if self.engine is None:
            log.warning("PostgreSQL engine not available. Skipping DB save.")
            return

        try:
            # 'if_exists=append' is key to avoid overwriting previous data
            df.to_sql('p2p_ads', self.engine, if_exists='append', index=False)
            log.debug("Data successfully pushed to PostgreSQL (table: p2p_ads).")
        except Exception as e:
            log.error(f"Error saving to PostgreSQL: {e}")

    def process_cycle_data(self, cycle_data):
        """
        Main entry point. Receives a list of dictionaries, 
        converts it to a DataFrame, and distributes it to storage handlers.
        """
        if not cycle_data:
            log.warning("No data received to save.")
            return

        df = pd.DataFrame(cycle_data)

        self.save_to_csv(df)
        self.save_to_db(df)
        
        log.info(f"Storage cycle complete: {len(cycle_data)} records secured.")