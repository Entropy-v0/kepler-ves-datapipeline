import pandas as pd
import datetime

def parse_announcements(json_data, page_num):
    extracted = []
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for item in json_data.get('data', []):

        try:

            methods = item['adv'].get('tradeMethods', [])
            bancos_lista = [m.get('tradeMethodName') for m in methods]
            bancos_string = ", ".join(bancos_lista)

            extracted.append({
                'timestamp': timestamp,
                'pagina': page_num,
                'cajero': item['advertiser']['nickName'],
                'bancos': bancos_string,
                'precio': float(item['adv']['price']),
                'min_vta': float(item['adv']['minSingleTransAmount']),
                "max_vta": float(item['adv']['maxSingleTransAmount']),
                "disponible": float(item['adv']['surplusAmount']),
                'ordenes': item['advertiser']['monthOrderCount'],
                'exito': item['advertiser']['monthFinishRate'] * 100
            })

        except (KeyError, TypeError) as e:
            continue

    return extracted