import config.settings as settings

def get_p2p_payload(page_num, trade_type="BUY",asset=None, fiat=None):
    """
    Construye el payload para Binance. 
    Permite sobrescribir el asset o fiat si el backend lo pide.
    """
    return {
        "asset": asset or settings.ASSET,
        "fiat": fiat or settings.FIAT,
        "merchantCheck": False,
        "page": page_num,
        "rows": 10,
        "tradeType": trade_type,
        "publisherType": "merchant",
        "filterType": "tradable",
        "classifies": ["mass", "profession", "fiat_trade"]
    }