from indicators import calculate_ema, calculate_rsi


def analyze_market(snapshot):
    prices = snapshot["closes"]
    price = snapshot["price"]

    ema_20 = calculate_ema(prices, 20)
    rsi_14 = calculate_rsi(prices, 14)

    classification = "no_trade"
    confidence = 50
    reasons = []
    invalidators = []

    if ema_20 is None or rsi_14 is None:
        invalidators.append("Not enough candle data")
    else:
        reasons.append(f"Price: {price}")
        reasons.append(f"EMA20: {round(ema_20, 2)}")
        reasons.append(f"RSI14: {round(rsi_14, 2)}")

        if price > ema_20 and rsi_14 < 70:
            classification = "pullback_long"
            confidence = 68
            reasons.append("Price above EMA20")
            reasons.append("RSI below overbought threshold")
        else:
            invalidators.append("No valid long setup")

    result = {
        "module": "market_analyst",
        "classification": classification,
        "confidence": confidence,
        "reasons": reasons,
        "invalidators": invalidators,
    }

    return result
