from market_data import get_market_snapshot
from market_analysis import analyze_market
from risk_manager_engine import evaluate_risk
from trade_execution import decide_execution
from post_generator import generate_post


def run_dirty_kid():
    account_state = {
        "open_position": False,
        "daily_trades": 0,
        "daily_loss_usd": 0,
        "system_paused": False,
    }

    snapshot = get_market_snapshot()
    analysis_result = analyze_market(snapshot)
    risk_result = evaluate_risk(analysis_result, account_state)
    execution_result = decide_execution(
        analysis_result, risk_result, snapshot, account_state
    )
    post_text = generate_post(execution_result, snapshot)

    result = {
        "snapshot": snapshot,
        "analysis": analysis_result,
        "risk": risk_result,
        "execution": execution_result,
        "post": post_text,
    }

    return result


if __name__ == "__main__":
    result = run_dirty_kid()
    print(result["snapshot"])
    print(result["analysis"])
    print(result["risk"])
    print(result["execution"])
    print(result["post"])
