import os
import time
import random
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

import signal
import threading

# Global event for graceful shutdown
shutdown_event = threading.Event()

def handle_exit(sig, frame):
    """
    Signal handler to trigger the shutdown event.
    """
    log.info(f"Signal {sig} received. Preparing to close resources...")
    shutdown_event.set()

# Register signals
signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

def run_cycle():
    """
    Orchestrates a single data collection cycle.
    """
    cycle_data = []
    log.info(f"Starting capture: {settings.PAGES} pages...")
    
    for p in range(1, settings.PAGES + 1):
        if shutdown_event.is_set():
            log.warning("Shutdown signal received during cycle. Aborting loop...")
            break

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

        # Interruptible sleep between pages
        if shutdown_event.wait(timeout=random.uniform(1.5, 3.5)):
            break

    if cycle_data:
        storage.process_cycle_data(cycle_data)

if __name__ == "__main__":
    log.info("--- Kepler Miner ONLINE ---")

    while not shutdown_event.is_set():
        try:
            run_cycle()
            
            if shutdown_event.is_set():
                break
                
            wait_time = random.randint(280, 340) 
            log.debug(f"Cycle completed. Next pulse in {wait_time} seconds...")
            
            # Interruptible sleep between cycles
            if shutdown_event.wait(timeout=wait_time):
                break
            
        except Exception as e:
            log.critical(f"Catastrophic failure in the orchestrator: {e}")
            log.info("Retrying resuscitation in 60 seconds...")
            if shutdown_event.wait(timeout=60):
                break

    log.info("Mining stopped gracefully. Closing collection and securing data.")