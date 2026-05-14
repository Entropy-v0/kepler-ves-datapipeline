import time
import random
import config.settings as settings
from core.scraper import fetch_page
from core.processor import parse_announcements
from core.storage import DataStorage
from core.services import get_p2p_payload
from core.logger import get_logger

log = get_logger("Kepler")
storage = DataStorage()

def run_cycle():
    """
    Orchestrates a single data collection cycle.
    """
    cycle_data = []
    log.info(f"Starting capture: {settings.PAGES} pages...")
    
    for p in range(1, settings.PAGES + 1):
        try:
            payload = get_p2p_payload(p, trade_type="BUY")
            
            json_data = fetch_page(payload)
        
            if json_data:
                announcements = parse_announcements(json_data, p)
                cycle_data.extend(announcements)
                log.debug(f"Page {p} processed ({len(announcements)} ads).")
            else:
                log.warning(f"Empty response on page {p}. Skipping...")
        
        except Exception as e:
            log.error(f"Error on page {p}: {e}")

        
        time.sleep(random.uniform(1.5, 3.5))

    storage.process_cycle_data(cycle_data)

if __name__ == "__main__":
    log.info("--- Kepler Miner ONLINE ---")

    while True:
        try:
            run_cycle()
            
            wait_time = random.randint(280, 340) 
            log.debug(f"Cycle completed. Next pulse in {wait_time} seconds...")
            time.sleep(wait_time)
            
        except KeyboardInterrupt:
            log.info("Mining stopped manually by the user. Closing collection.")
            break
        except Exception as e:
            log.critical(f"Catastrophic failure in the orchestrator: {e}")
            log.info("Retrying resuscitation in 60 seconds...")
            time.sleep(60)