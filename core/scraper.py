import requests
import random
from config.settings import URL, USER_AGENTS

def fetch_page(payload):

    headers = {'User-Agent': random.choice(USER_AGENTS)}

    try:
        
        response = requests.post(URL, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        print(f"Error en red: {e}")
        return None