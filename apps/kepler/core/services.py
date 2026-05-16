import config.settings as settings

def get_p2p_payload(page_num, trade_type="BUY",asset=None, fiat=None, banks=None):
    """
    Builds the payload for Binance P2P API.
    Allows overriding asset or fiat if requested by the backend.
    """
    return {
        "asset": asset or settings.ASSET,
        "fiat": fiat or settings.FIAT,
        "merchantCheck": False,
        "page": page_num,
        "rows": 20,
        "tradeType": trade_type,
        "publisherType": "merchant",
        "filterType": "tradable",
        "payTypes": banks or [],
        "classifies": ["mass", "profession", "fiat_trade"]
    }