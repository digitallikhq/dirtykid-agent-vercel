import json
import random

def calculate_ema(prices, period=20):
    k = 2 / (period + 1)
    ema = prices[0]
    for price in prices[1:]:
        ema = price * k + ema * (1 - k)
    return round(ema, 2)

def calculate_rsi(prices, period=14):
    gains = []
    losses = []

    for i in range(1, len(prices)):
        diff = prices[i] - prices[i - 1]

        if diff > 0:
            gains.append(diff)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(diff))

    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period if sum(losses[-period:]) != 0 else 0.0001

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return round(rsi, 2)

def handler(request):

    # Ignore favicon requests
    if request.path == "/favicon.ico":
        return {
            "statusCode": 204,
            "body": ""
        }

    base_price = 71400
    price = base_price + random.uniform(-100, 100)

    closes = []
    for i in range(21):
        closes.append(base_price - 200 + i * 10 + random.uniform(-20, 20))

    closes[-1] = price

    ema20 = calculate_ema(closes)
    rsi14 = calculate_rsi(closes)

    decision = "HOLD"

    if price > ema20 and rsi14 < 65:
        decision = "LONG"

    if rsi14 > 75:
        decision = "NO_TRADE"

    response = {
        "status": "ok",
        "snapshot": {
            "symbol": "BTC-USD",
            "price": round(price, 2)
        },
        "analysis": {
            "EMA20": ema20,
            "RSI14": rsi14,
            "decision": decision
        }
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(response)
    }
