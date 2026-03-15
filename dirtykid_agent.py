from market_data import get_market_snapshot
from market_analysis import analyze_market
from risk_manager_engine import evaluate_risk
from trade_execution import decide_execution
from post_generator import generate_post
from paper_trade_logger import log_paper_trade


def run_dirty_kid():

    account_state = {
        "open_position": False,
        "daily_trades": 0,
        "daily_loss_usd": 0,
        "system_paused": False,
    }

    snapshot = get_market_snapshot()

    analysis_result = analyze_market(snapshot)

    risk_result = evaluate_risk(
        analysis_result,
        account_state
    )

    execution_result = decide_execution(
        analysis_result,
        risk_result,
        snapshot,
        account_state
    )

    post_text = generate_post(
        execution_result,
        snapshot
    )

    log_entry = log_paper_trade(
        snapshot,
        analysis_result,
        risk_result,
        execution_result
    )

    return {
        "status": "ok",
        "snapshot": snapshot,
        "analysis": analysis_result,
        "risk": risk_result,
        "execution": execution_result,
        "post": post_text,
        "paper_trade_log_entry": log_entry
    }
