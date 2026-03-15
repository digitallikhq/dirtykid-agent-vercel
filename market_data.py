import requests


COINBASE_CANDLES = "https://api.exchange.coinbase.com/products/BTC-USD/candles"


def get_btc_spot_price():
    url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
    return float(data["data"]["amount"])


def get_btc_candles():
    params = {
        "granularity": 60,
        "limit": 100
    }

    r = requests.get(COINBASE_CANDLES, params=params, timeout=10)
    r.raise_for_status()

    candles = r.json()

    closes = []

    for candle in candles:
        close_price = candle[4]
        closes.append(close_price)

    closes.reverse()

    return closes


def get_market_snapshot():
    price = get_btc_spot_price()
    closes = get_btc_candles()

    snapshot = {
        "symbol": "BTC-USD",
        "price": price,
        "closes": closes,
        "data_version": "COINBASE_LIVE"
    }

    return snapshot
