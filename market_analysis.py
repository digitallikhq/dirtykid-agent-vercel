def analyze_market(snapshot):
    price = snapshot["price"]

    if price > 0:
        classification = "no_trade"
        confidence = 50
        reasons = ["Live price received", "Strategy logic not connected yet"]
        invalidators = ["No indicator engine yet", "No candle history yet"]
    else:
        classification = "no_trade"
        confidence = 0
        reasons = ["Invalid price data"]
        invalidators = ["Price feed failure"]

    result = {
        "module": "market_analyst",
        "classification": classification,
        "confidence": confidence,
        "reasons": reasons,
        "invalidators": invalidators,
    }

    return result
