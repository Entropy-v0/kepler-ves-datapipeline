import pandas as pd
import os

# Paths
OLD_FILE = "output/historial_p2p.csv"
NEW_FILE = "output/p2p_history.csv"

# Column mapping
COLUMN_MAPPING = {
    'timestamp': 'timestamp',
    'pagina': 'page',
    'cajero': 'merchant',
    'bancos': 'banks',
    'precio': 'price',
    'min_vta': 'min_limit',
    'max_vta': 'max_limit',
    'disponible': 'available',
    'ordenes': 'orders',
    'exito': 'success_rate'
}

def migrate():
    """
    Handles the migration of existing P2P data from Spanish to English format.
    
    This function:
    1. Checks for the existence of the old CSV file ('historial_p2p.csv').
    2. Loads the data using pandas.
    3. Renames the columns using the predefined mapping.
    4. Saves the updated data to the new English filename ('p2p_history.csv').
    5. Backs up the old file by renaming it to '.bak'.
    """
    if not os.path.exists(OLD_FILE):
        print(f"File {OLD_FILE} not found. Skipping migration.")
        return

    print(f"Reading {OLD_FILE}...")
    df = pd.read_csv(OLD_FILE)
    
    # Check if headers actually match the old ones
    existing_cols = df.columns.tolist()
    print(f"Existing columns: {existing_cols}")
    
    # Rename columns that exist in the mapping
    df.rename(columns=COLUMN_MAPPING, inplace=True)
    
    print(f"Saving to {NEW_FILE} with new headers...")
    df.to_csv(NEW_FILE, index=False)
    
    print("Migration successful.")
    
    # Optional: rename old file to backup
    backup_file = OLD_FILE + ".bak"
    os.rename(OLD_FILE, backup_file)
    print(f"Old file renamed to {backup_file}")

if __name__ == "__main__":
    migrate()
