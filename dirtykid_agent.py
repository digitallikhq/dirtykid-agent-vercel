from datetime import datetime

from market_data import get_market_snapshot
from market_analysis import analyze_market
from risk_manager_engine import evaluate_risk
from trade_execution import decide_execution
from post_generator import generate_post

try:
    from paper_trade_logger import log_paper_trade
except Exception:
    log_paper_trade = None

try:
    from supabase_logger import log_to_supabase
except Exception:
    log_to_supabase = None

try:
    from state_manager import get_mode
except Exception:
    def get_mode():
        return "paper"


def run_dirty_kid():
    account_state = {
        "open_position": False,
        "daily_trades": 0,
        "daily_loss_usd": 0,
        "system_paused": False,
    }

    mode = get_mode()

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

    log_entry = {
        "timestamp_utc": datetime.utcnow().isoformat(),
        "symbol": snapshot.get("symbol"),
        "price": snapshot.get("price"),
        "data_version": snapshot.get("data_version"),
        "classification": analysis_result.get("classification"),
        "confidence": analysis_result.get("confidence"),
        "analysis_reasons": analysis_result.get("reasons", []),
        "analysis_invalidators": analysis_result.get("invalidators", []),
        "risk_approved": risk_result.get("approved"),
        "risk_blocks": risk_result.get("blocks", []),
        "action": execution_result.get("action"),
        "execution_reason": execution_result.get("reason"),
        "post_needed": execution_result.get("post_needed"),
        "mode": mode,
    }

    local_log_status = {"status": "inactive"}
    if log_paper_trade is not None:
        try:
            log_paper_trade(
                snapshot,
                analysis_result,
                risk_result,
                execution_result
            )
            local_log_status = {"status": "ok"}
        except Exception as e:
            local_log_status = {
                "status": "error",
                "reason": str(e)
            }

    supabase_status = {"status": "inactive"}
    if log_to_supabase is not None:
        try:
            supabase_status = log_to_supabase(
                snapshot,
                analysis_result,
                risk_result,
                execution_result,
                mode
            )
        except Exception as e:
            supabase_status = {
                "status": "error",
                "reason": str(e)
            }

    return {
        "status": "ok",
        "agent_version": "FULL_NO_API_V2",
        "mode": mode,
        "snapshot": snapshot,
        "analysis": analysis_result,
        "risk": risk_result,
        "execution": execution_result,
        "post": post_text,
        "paper_trade_log_entry": log_entry,
        "local_log_status": local_log_status,
        "supabase_status": supabase_status
    }
