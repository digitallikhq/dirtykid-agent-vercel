import json
import random
import math
from http.server import BaseHTTPRequestHandler


def calculate_ema(prices, period=20):
    if len(prices) < period:
        return sum(prices) / len(prices)

    k = 2 / (period + 1)
    ema = prices[0]

    for price in prices[1:]:
        ema = price * k + ema * (1 - k)

    return round(ema, 2)


def calculate_rsi(prices, period=14):
    if len(prices) <= period:
        return 50

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
    avg_loss = sum(losses[-period:]) / period

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return round(rsi, 2)


class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        # Prevent favicon crash
        if self.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return

        # Simulated BTC price
        base_price = 71400
        price = base_price + random.uniform(-100, 100)

        closes = []

        for i in range(21):
            closes.append(base_price - 200 + i * 10 + random.uniform(-20, 20))

        closes[-1] = price

        ema20 = calculate_ema(closes, 20)
        rsi14 = calculate_rsi(closes, 14)

        decision = "HOLD"

        if price > ema20 and rsi14 < 65:
            decision = "LONG"

        if rsi14 > 75:
            decision = "NO_TRADE"

        response = {
            "status": "ok",
            "snapshot": {
                "symbol": "BTC-USD",
                "price": round(price, 2),
                "closes": closes
            },
            "analysis": {
                "EMA20": ema20,
                "RSI14": rsi14,
                "decision": decision
            }
        }

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps(response).encode())
