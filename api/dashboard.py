from http.server import BaseHTTPRequestHandler
from dirtykid_agent import run_dirty_kid


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return

        result = run_dirty_kid()

        snapshot = result.get("snapshot", {})
        analysis = result.get("analysis", {})
        risk = result.get("risk", {})
        execution = result.get("execution", {})
        post = result.get("post", "No log")

        reasons = "<br>".join(analysis.get("reasons", [])) or "None"
        invalidators = "<br>".join(analysis.get("invalidators", [])) or "None"
        risk_reasons = "<br>".join(risk.get("reasons", [])) or "None"
        blocks = "<br>".join(risk.get("blocks", [])) or "None"

        html = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Dirty Kid Agent</title>
  <style>
    body {{
      margin: 0;
      background: #0b0f14;
      color: #ffffff;
      font-family: Arial, Helvetica, sans-serif;
      padding: 24px;
    }}
    .card {{
      max-width: 900px;
      margin: auto;
      background: #0f1620;
      border-radius: 14px;
      padding: 24px;
      box-shadow: 0 0 20px rgba(0,0,0,0.45);
    }}
    .title {{
      font-size: 30px;
      font-weight: bold;
      margin-bottom: 16px;
    }}
    .section {{
      margin-top: 20px;
      padding-top: 16px;
      border-top: 1px solid #1f2b38;
    }}
    .section-title {{
      font-size: 18px;
      font-weight: bold;
      margin-bottom: 10px;
    }}
    .log {{
      background: #111822;
      padding: 12px;
      border-radius: 8px;
      white-space: pre-line;
      margin-top: 8px;
    }}
    .row {{
      margin-bottom: 8px;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="title">Dirty Kid Agent</div>

    <div class="row"><strong>Status:</strong> {result.get("status", "N/A")}</div>
    <div class="row"><strong>Symbol:</strong> {snapshot.get("symbol", "N/A")}</div>
    <div class="row"><strong>BTC Price:</strong> ${snapshot.get("price", "N/A")}</div>
    <div class="row"><strong>Data Version:</strong> {snapshot.get("data_version", "N/A")}</div>

    <div class="section">
      <div class="section-title">Market Analysis</div>
      <div class="row"><strong>Classification:</strong> {analysis.get("classification", "N/A")}</div>
      <div class="row"><strong>Confidence:</strong> {analysis.get("confidence", "N/A")}</div>
      <div class="row"><strong>Reasons:</strong><br>{reasons}</div>
      <div class="row"><strong>Invalidators:</strong><br>{invalidators}</div>
    </div>

    <div class="section">
      <div class="section-title">Risk Manager</div>
      <div class="row"><strong>Approved:</strong> {risk.get("approved", "N/A")}</div>
      <div class="row"><strong>Position Size:</strong> ${risk.get("position_size_usd", "N/A")}</div>
      <div class="row"><strong>Stop Loss:</strong> {risk.get("stop_loss_pct", "N/A")}%</div>
      <div class="row"><strong>Take Profit:</strong> {risk.get("take_profit_pct", "N/A")}%</div>
      <div class="row"><strong>Risk Reasons:</strong><br>{risk_reasons}</div>
      <div class="row"><strong>Blocks:</strong><br>{blocks}</div>
    </div>

    <div class="section">
      <div class="section-title">Execution Gate</div>
      <div class="row"><strong>Action:</strong> {execution.get("action", "N/A")}</div>
      <div class="row"><strong>Symbol:</strong> {execution.get("symbol", "N/A")}</div>
      <div class="row"><strong>Position Size:</strong> ${execution.get("position_size_usd", "N/A")}</div>
      <div class="row"><strong>Reason:</strong> {execution.get("reason", "N/A")}</div>
      <div class="row"><strong>Post Needed:</strong> {execution.get("post_needed", "N/A")}</div>
    </div>

    <div class="section">
      <div class="section-title">Agent Log</div>
      <div class="log">{post}</div>
    </div>
  </div>
</body>
</html>
"""

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))
