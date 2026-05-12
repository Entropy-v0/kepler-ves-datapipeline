import time
import random
import os
import pandas as pd
from core.scraper import fetch_page
from core.processor import parse_announcements
import config.settings as settings
from core.logger import get_logger


log = get_logger("Kepler")

def run_cycle():
    """
    Orchestrates a single data collection cycle.
    
    This function performs the following steps:
    1. Iterates through the number of pages defined in settings.
    2. Fetches each page from the Binance P2P API.
    3. Parses the announcements from the JSON response.
    4. Aggregates all data and saves it to a CSV file.
    5. Implements random delays between requests to avoid rate limiting.
    """
    cycle_data = []
    
    log.info(f"Starting capture: {settings.PAGES} pages...")
    
    for p in range(1, settings.PAGES + 1):

        payload = {
            "asset": settings.ASSET,
            "fiat": settings.FIAT,
            "merchantCheck": False,
            "page": p,
            "rows": 10,
            "tradeType": "BUY",
            "publisherType": "merchant",
            "filterType": "tradable",
            "classifies": ["mass", "profession", "fiat_trade"]
        }
        
        try:
            json_data = fetch_page(payload)
        
            if json_data:
                announcements = parse_announcements(json_data, p)
                cycle_data.extend(announcements)
                log.debug(f"Page {p} processed ({len(announcements)} announcements).")
            else:
                log.warning(f"Empty response on page {p}. Skipping...")
        
        except Exception as e:
            log.error(f"Critical error on page {p}: {e}")

        time.sleep(random.uniform(1.5, 3.5))

    if cycle_data:
        df = pd.DataFrame(cycle_data)
        exists = os.path.isfile(settings.OUTPUT_FILE)
        df.to_csv(settings.OUTPUT_FILE, mode='a', index=False, header=not exists)
        log.info(f"Cycle completed. {len(cycle_data)} announcements dumped to {settings.OUTPUT_FILE}")
    else:
        log.warning("Cycle finished without data collected.")


if __name__ == "__main__":
    log.info("--- Kepler Miner ONLINE ---")

    while True:
        try:
            run_cycle()
            
            wait_time = random.randint(280, 340) 
            log.debug(f"Waiting. Next pulse in {wait_time} seconds...")
            time.sleep(wait_time)
            
        except KeyboardInterrupt:
            log.info("Mining stopped manually by the user. Closing data collection.")
            break
        except Exception as e:
            log.critical(f"Catastrophic failure in the orchestrator: {e}")
            log.info("Retrying resuscitation in 60 seconds...")
            time.sleep(60)