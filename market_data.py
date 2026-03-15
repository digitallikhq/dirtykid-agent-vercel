import requests


def get_btc_spot_price():
    url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    return float(data["data"]["amount"])


def get_mock_closes(current_price):
    return [
        current_price - 220,
        current_price - 180,
        current_price - 210,
        current_price - 170,
        current_price - 160,
        current_price - 175,
        current_price - 140,
        current_price - 130,
        current_price - 145,
        current_price - 115,
        current_price - 105,
        current_price - 120,
        current_price - 90,
        current_price - 85,
        current_price - 95,
        current_price - 70,
        current_price - 68,
        current_price - 66,
        current_price - 64,
        current_price - 62,
        current_price
    ]


def get_market_snapshot():
    price = get_btc_spot_price()
    closes = get_mock_closes(price)

    snapshot = {
        "symbol": "BTC-USD",
        "price": price,
        "closes": closes,
        "data_version": "MOCK_V4"
    }

    return snapshot
