import html
import json
import traceback
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == "/favicon.ico":
                self.send_response(204)
                self.end_headers()
                return

            from dirtykid_agent import run_dirty_kid

            result = run_dirty_kid()

            snapshot = result.get("snapshot", {})
            analysis = result.get("analysis", {})
            risk = result.get("risk", {})
            execution = result.get("execution", {})
            post = result.get("post", "No log")

            reasons = "<br>".join(
                html.escape(str(x)) for x in analysis.get("reasons", [])
            ) or "None"

            invalidators = "<br>".join(
                html.escape(str(x)) for x in analysis.get("invalidators", [])
            ) or "None"

            blocks = "<br>".join(
                html.escape(str(x)) for x in risk.get("blocks", [])
            ) or "None"

            page = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Dirty Kid Agent</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {{
      margin: 0;
      padding: 20px;
      background: #0b0f14;
      color: #ffffff;
      font-family: Arial, Helvetica, sans-serif;
    }}
    .wrap {{
      max-width: 900px;
      margin: 0 auto;
      background: #111821;
      border-radius: 14px;
      padding: 24px;
      box-shadow: 0 0 20px rgba(0,0,0,.35);
    }}
    .title {{
      font-size: 28px;
      font-weight: 700;
      margin-bottom: 16px;
    }}
    .section {{
      margin-top: 18px;
      padding-top: 18px;
      border-top: 1px solid #1e293b;
    }}
    .section-title {{
      font-size: 18px;
      font-weight: 700;
      margin-bottom: 8px;
    }}
    .log {{
      background: #0b0f14;
      padding: 12px;
      border-radius: 8px;
      white-space: pre-line;
    }}
    .buy {{
      color: #22c55e;
      font-weight: 700;
    }}
    .hold {{
      color: #facc15;
      font-weight: 700;
    }}
    .pause {{
      color: #f97316;
      font-weight: 700;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="title">Dirty Kid Agent</div>

    <div><strong>Status:</strong> {html.escape(str(result.get("status", "N/A")))}</div>
    <div><strong>Symbol:</strong> {html.escape(str(snapshot.get("symbol", "N/A")))}</div>
    <div><strong>BTC Price:</strong> ${snapshot.get("price", "N/A")}</div>
    <div><strong>Data Version:</strong> {html.escape(str(snapshot.get("data_version", "N/A")))}</div>

    <div class="section">
      <div class="section-title">Market Analysis</div>
      <div><strong>Classification:</strong> {html.escape(str(analysis.get("classification", "N/A")))}</div>
      <div><strong>Confidence:</strong> {html.escape(str(analysis.get("confidence", "N/A")))}</div>
      <div style="margin-top:10px;"><strong>Reasons:</strong><br>{reasons}</div>
      <div style="margin-top:10px;"><strong>Invalidators:</strong><br>{invalidators}</div>
    </div>

    <div class="section">
      <div class="section-title">Risk Manager</div>
      <div><strong>Approved:</strong> {html.escape(str(risk.get("approved", "N/A")))}</div>
      <div><strong>Position Size:</strong> ${html.escape(str(risk.get("position_size_usd", "N/A")))}</div>
      <div><strong>Stop Loss:</strong> {html.escape(str(risk.get("stop_loss_pct", "N/A")))}%</div>
      <div><strong>Take Profit:</strong> {html.escape(str(risk.get("take_profit_pct", "N/A")))}%</div>
      <div style="margin-top:10px;"><strong>Blocks:</strong><br>{blocks}</div>
    </div>

    <div class="section">
      <div class="section-title">Execution</div>
      <div><strong>Action:</strong> <span class="{html.escape(str(execution.get("action", "N/A"))).lower()}">{html.escape(str(execution.get("action", "N/A")))}</span></div>
      <div><strong>Reason:</strong> {html.escape(str(execution.get("reason", "N/A")))}</div>
      <div><strong>Post Needed:</strong> {html.escape(str(execution.get("post_needed", "N/A")))}</div>
    </div>

    <div class="section">
      <div class="section-title">Agent Log</div>
      <div class="log">{html.escape(str(post))}</div>
    </div>
  </div>
</body>
</html>"""

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(page.encode("utf-8"))

        except Exception:
            error = {
                "status": "error",
                "traceback": traceback.format_exc()
            }
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(error).encode("utf-8"))
