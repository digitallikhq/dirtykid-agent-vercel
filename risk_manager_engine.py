def evaluate_risk(analysis_result, account_state):
    approved = False
    reasons = []
    blocks = []

    if analysis_result["classification"] == "no_trade":
        blocks.append("No valid trade setup")
    else:
        reasons.append("Valid setup detected")

    if account_state["open_position"]:
        blocks.append("Position already open")

    if account_state["daily_trades"] >= 2:
        blocks.append("Daily trade limit reached")

    if account_state["daily_loss_usd"] >= 5:
        blocks.append("Daily loss limit reached")

    if not blocks:
        approved = True

    result = {
        "module": "risk_manager",
        "approved": approved,
        "position_size_usd": 10,
        "stop_loss_pct": 1.0,
        "take_profit_pct": 2.0,
        "reasons": reasons,
        "blocks": blocks,
    }

    return result
