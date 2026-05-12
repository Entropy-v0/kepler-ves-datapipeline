import requests
import random
from config.settings import URL, USER_AGENTS
from core.logger import get_logger

log = get_logger("Kepler")

def fetch_page(payload):
    """
    Sends a POST request to the Binance P2P API to retrieve a list of advertisements.
    
    Args:
        payload (dict): The request body containing search criteria (asset, fiat, page, etc.).
        
    Returns:
        dict or None: The JSON response as a dictionary if successful, or None if the 
                      request fails or encounters an error.
    """

    headers = {'User-Agent': random.choice(USER_AGENTS)}

    try:
        
        response = requests.post(URL, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        log.error(f"Network error: {e}")
        return None