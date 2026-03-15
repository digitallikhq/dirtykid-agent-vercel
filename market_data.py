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
        current_price - 200,
        current_price - 210,
        current_price - 190,
        current_price - 170,
        current_price - 150,
        current_price - 140,
        current_price - 130,
        current_price - 120,
        current_price - 110,
        current_price - 100,
        current_price - 90,
        current_price - 85,
        current_price - 80,
        current_price - 70,
        current_price - 60,
        current_price - 55,
        current_price - 50,
        current_price - 45,
        current_price - 40,
        current_price
    ]

def get_market_snapshot():
    price = get_btc_spot_price()
    closes = get_mock_closes(price)

    snapshot = {
        "symbol": "BTC-USD",
        "price": price,
        "closes": closes
    }

    return snapshot
