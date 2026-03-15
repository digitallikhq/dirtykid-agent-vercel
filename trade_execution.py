def decide_execution(analysis_result, risk_result, snapshot, account_state):
    action = "HOLD"
    reason = "No valid action"
    post_needed = False

    if account_state["system_paused"]:
        action = "PAUSE"
        reason = "System is paused"
    elif risk_result["approved"] and not account_state["open_position"]:
        action = "BUY"
        reason = "Risk approved and no open position"
        post_needed = True

    result = {
        "module": "execution_gate",
        "action": action,
        "symbol": snapshot["symbol"],
        "position_size_usd": 10,
        "reason": reason,
        "post_needed": post_needed,
    }

    return result
