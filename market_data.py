import requests


def get_btc_spot_price():
    url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    return float(data["data"]["amount"])


def get_mock_closes(current_price):
    closes = []
    base = current_price - 300

    for i in range(20):
        closes.append(base + (i * 15))

    closes.append(current_price)
    return closes


def get_market_snapshot():
    price = get_btc_spot_price()
    closes = get_mock_closes(price)

    snapshot = {
        "symbol": "BTC-USD",
        "price": price,
        "closes": closes
    }

    return snapshot
