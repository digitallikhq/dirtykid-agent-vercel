import requests

def get_btc_spot_price():
    url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    return float(data["data"]["amount"])

def get_market_snapshot():
    price = get_btc_spot_price()

    snapshot = {
        "symbol": "BTC-USD",
        "price": price
    }

    return snapshot
