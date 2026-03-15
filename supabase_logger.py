import os


def log_to_supabase(snapshot, analysis, risk, execution, mode):
    try:
        from supabase import create_client
    except Exception:
        return {
            "status": "inactive",
            "reason": "supabase package not available"
        }

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not supabase_url or not supabase_key:
        return {
            "status": "inactive",
            "reason": "missing supabase environment variables"
        }

    try:
        client = create_client(supabase_url, supabase_key)

        payload = {
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
            "mode": mode,
        }

        result = client.table("paper_trades").insert(payload).execute()

        return {
            "status": "ok",
            "data": result.data
        }

    except Exception as e:
        return {
            "status": "error",
            "reason": str(e)
        }
