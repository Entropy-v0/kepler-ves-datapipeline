import requests
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config.settings import URL, USER_AGENTS
from core.logger import get_logger

log = get_logger("Kepler")

def get_secure_session():
    """
    Configures a requests session with an exponential backoff retry strategy.
    """
    session = requests.Session()
    
    # Configure retry strategy: 3 retries, exponential backoff, retry on specific status codes
    retry_strategy = Retry(
        total=3,
        backoff_factor=1.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"]
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    
    return session

def fetch_page(payload):
    """
    Sends a POST request to the Binance P2P API with retry logic.
    """
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    session = get_secure_session()

    try:
        log.debug(f"Fetching page {payload.get('page')}...")
        response = session.post(URL, json=payload, headers=headers, timeout=20)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as e:
        log.error(f"HTTP Error (possible block or API change): {e}")
    except requests.exceptions.ConnectionError as e:
        log.error(f"Connection error (network down?): {e}")
    except requests.exceptions.Timeout as e:
        log.error(f"Timeout exceeded during request: {e}")
    except Exception as e:
        log.error(f"Unexpected error in scraper: {e}")
    
    return None