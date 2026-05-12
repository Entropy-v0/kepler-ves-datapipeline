import pandas as pd
import datetime

def parse_announcements(json_data, page_num):
    """
    Parses raw JSON data from the Binance P2P API into a list of structured dictionaries.
    
    Args:
        json_data (dict): The raw JSON response from the API.
        page_num (int): The current page number being processed (for metadata).
        
    Returns:
        list: A list of dictionaries, each containing extracted information such as 
              merchant name, price, limits, and payment methods.
    """
    extracted = []
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for item in json_data.get('data', []):

        try:

            methods = item['adv'].get('tradeMethods', [])
            banks_list = [m.get('tradeMethodName') for m in methods]
            banks_string = ", ".join(banks_list)

            extracted.append({
                'timestamp': timestamp,
                'page': page_num,
                'merchant': item['advertiser']['nickName'],
                'banks': banks_string,
                'price': float(item['adv']['price']),
                'min_limit': float(item['adv']['minSingleTransAmount']),
                "max_limit": float(item['adv']['maxSingleTransAmount']),
                "available": float(item['adv']['surplusAmount']),
                'orders': item['advertiser']['monthOrderCount'],
                'success_rate': item['advertiser']['monthFinishRate'] * 100
            })

        except (KeyError, TypeError) as e:
            continue

    return extracted