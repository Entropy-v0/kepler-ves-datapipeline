import os
import time
import random
import signal
import threading
from dotenv import load_dotenv

load_dotenv()

import config.settings as settings
from core.scraper import fetch_page
from core.processor import parse_announcements
from core.storage import DataStorage
from core.services import get_p2p_payload
from core.logger import get_logger

log = get_logger("Kepler")
storage = DataStorage()

# Global event for graceful shutdown
shutdown_event = threading.Event()

def handle_exit(sig, frame):
    log.info(f"Signal {sig} received. Preparing to close resources...")
    shutdown_event.set()

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

def run_cycle():
    """
    Orchestrates a collection cycle for both market sides (BUY and SELL).
    """
    # Define both market sides
    market_sides = ["BUY", "SELL"]
    
    for side in market_sides:
        if shutdown_event.is_set():
            break
            
        side_data = []
        log.info(f"Starting capture cycle for SIDE: {side} ({settings.PAGES} pages)...")
        
        for p in range(1, settings.PAGES + 1):
            if shutdown_event.is_set():
                log.warning(f"Shutdown signal received. Aborting {side} loop...")
                break

            try:
                # 1. Get specific payload for current side
                payload = get_p2p_payload(p, trade_type=side)
                
                # 2. API Request
                json_data = fetch_page(payload)
            
                if json_data:
                    # 3. Process injecting 'side' (BUY/SELL) and 'fiat' from payload
                    fiat = payload.get("fiat", "VES")
                    announcements = parse_announcements(json_data, p, side, fiat)
                    side_data.extend(announcements)
                    log.debug(f"[{side}] Page {p} processed ({len(announcements)} ads).")
                else:
                    log.warning(f"[{side}] Empty response on page {p}.")
            
            except Exception as e:
                log.error(f"Error on page {p} [{side}]: {e}")

            # Random sleep between pages to avoid rate limiting
            if shutdown_event.wait(timeout=random.uniform(1.5, 3.5)):
                break

        # 4. Persistence: Save this side's block before proceeding to the next
        if side_data:
            storage.process_cycle_data(side_data)
            log.info(f"Successfully secured {len(side_data)} records for {side}.")

if __name__ == "__main__":
    log.info("--- Kepler Miner ONLINE (Dual Mode) ---")

    while not shutdown_event.is_set():
        try:
            run_cycle()
            
            if shutdown_event.is_set():
                break
                
            # Sleep between full cycles (approx 5 min)
            wait_time = random.randint(280, 340) 
            log.debug(f"Full cycle completed. Next dual pulse in {wait_time} seconds...")
            
            if shutdown_event.wait(timeout=wait_time):
                break
            
        except Exception as e:
            log.critical(f"Catastrophic failure in the orchestrator: {e}")
            log.info("Retrying resuscitation in 60 seconds...")
            if shutdown_event.wait(timeout=60):
                break

    log.info("Mining stopped gracefully. Closing collection and securing data.")