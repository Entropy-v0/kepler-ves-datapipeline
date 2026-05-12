import time
import random
import os
import pandas as pd
from core.scraper import fetch_page
from core.processor import parse_announcements
import config.settings as settings

def ejecutar_ciclo():
    """Ejecuta una ráfaga de captura de 5 páginas (50 anuncios)."""
    datos_ciclo = []
    
    print(f"\nIniciando captura: {settings.PAGINAS} páginas...")
    
    for p in range(1, settings.PAGINAS + 1):

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
        
        json_data = fetch_page(payload)
        
        if json_data:
            anuncios = parse_announcements(json_data, p)
            datos_ciclo.extend(anuncios)
            print(f"Página {p} capturada ({len(anuncios)} anuncios).")
        else:
            print(f"Fallo en página {p}. Saltando...")
        
        time.sleep(random.uniform(1.5, 3.5))

    if datos_ciclo:
        df = pd.DataFrame(datos_ciclo)
        existe = os.path.isfile(settings.ARCHIVO_SALIDA)
        df.to_csv(settings.ARCHIVO_SALIDA, mode='a', index=False, header=not existe)
        print(f"Total: {len(datos_ciclo)} anuncios guardados en {settings.ARCHIVO_SALIDA}")
    else:
        print("No se recolectaron datos en este ciclo.")


if __name__ == "__main__":
    print("Minero del Tártaro ONLINE")

    while True:
        try:
            ejecutar_ciclo()
            
            espera = random.randint(280, 340) 
            print(f"Durmiendo por {espera} segundos...")
            time.sleep(espera)
            
        except KeyboardInterrupt:
            print("\n Minería detenida por el usuario. Saliendo...")
            break
        except Exception as e:
            print(f"\n Error inesperado en el orquestador: {e}")
            print("Reintentando en 60 segundos...")
            time.sleep(60)