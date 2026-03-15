import json
from datetime import datetime
from pathlib import Path


LOG_PATH = Path("logs/paper_trades.json")


def log_paper_trade(snapshot, analysis, risk, execution):

    entry = {
        "timestamp_utc": datetime.utcnow().isoformat(),
        "symbol": snapshot.get("symbol"),
        "price": snapshot.get("price"),
        "data_version": snapshot.get("data_version"),

        "classification": analysis.get("classification"),
        "confidence": analysis.get("confidence"),
        "analysis_reasons": analysis.get("reasons", []),
        "analysis_invalidators": analysis.get("invalidators", []),

        "risk_approved": risk.get("approved"),
        "risk_blocks": risk.get("blocks", []),

        "action": execution.get("action"),
        "execution_reason": execution.get("reason"),
        "post_needed": execution.get("post_needed"),
    }

    if not LOG_PATH.exists():
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        LOG_PATH.write_text("[]", encoding="utf-8")

    try:
        existing = json.loads(LOG_PATH.read_text(encoding="utf-8"))

        if not isinstance(existing, list):
            existing = []

    except Exception:
        existing = []

    existing.append(entry)

    # keep last 200 logs
    existing = existing[-200:]

    LOG_PATH.write_text(
        json.dumps(existing, indent=2),
        encoding="utf-8"
    )

    return entry
