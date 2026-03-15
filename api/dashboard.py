import html
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

            reasons = "<br>".join(html.escape(str(x)) for x in analysis.get("reasons", [])) or "None"
            invalidators = "<br>".join(html.escape(str(x)) for x in analysis.get("invalidators", [])) or "None"
            blocks = "<br>".join(html.escape(str(x)) for x in risk.get("blocks", [])) or "None"

            price = snapshot.get("price", "N/A")
            symbol = html.escape(str(snapshot.get("symbol", "N/A")))
            data_version = html.escape(str(snapshot.get("data_version", "N/A")))
            classification = html.escape(str(analysis.get("classification", "N/A")))
            confidence = html.escape(str(analysis.get("confidence", "N/A")))
            approved = html.escape(str(risk.get("approved", "N/A")))
            position_size = html.escape(str(risk.get("position_size_usd", "N/A")))
            stop_loss = html.escape(str(risk.get("stop_loss_pct", "N/A")))
            take_profit = html.escape(str(risk.get("take_profit_pct", "N/A")))
            action = html.escape(str(execution.get("action", "N/A")))
            reason = html.escape(str(execution.get("reason", "N/A")))
            post_needed = html.escape(str(execution.get("post_needed", "N/A")))
            post_text = html.escape(str(post))

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
    .ok {{
      color: #22c55e;
      font-weight: 700;
    }}
    .buy {{
      color: #22c55e;
      font-weight: 700;
    }}
    .hold {{
      color: #facc15;
      font-weight: 700;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="title">Dirty Kid Agent</div>

    <div><strong>Status:</strong> <span class="ok">{html.escape(str(result.get("status", "N/A")))}</span></div>
    <div><strong>Symbol:</strong> {symbol}</div>
    <div><strong>BTC Price:</strong> ${price}</div>
    <div><strong>Data Version:</strong> {data_version}</div>

    <div class="section">
      <div class="section-title">Market Analysis</div>
      <div><strong>Classification:</strong> {classification}</div>
      <div><strong>Confidence:</strong> {confidence}</div>
      <div style="margin-top:10px;"><strong>Reasons:</strong><br>{reasons}</div>
      <div style="margin-top:10px;"><strong>Invalidators:</strong><br>{invalidators}</div>
    </div>

    <div class="section">
      <div class="section-title">Risk Manager</div>
      <div><strong>Approved:</strong> {approved}</div>
      <div><strong>Position Size:</strong> ${position_size}</div>
      <div><strong>Stop Loss:</strong> {stop_loss}%</div>
      <div><strong>Take Profit:</strong> {take_profit}%</div>
      <div style="margin-top:10px;"><strong>Blocks:</strong><br>{blocks}</div>
    </div>

    <div class="section">
      <div class="section-title">Execution</div>
      <div><strong>Action:</strong> <span class="{action.lower()}">{action}</span></div>
      <div><strong>Reason:</strong> {reason}</div>
      <div><strong>Post Needed:</strong> {post_needed}</div>
    </div>

    <div class="section">
      <div class="section-title">Agent Log</div>
      <div class="log">{post_text}</div>
    </div>
  </div>
</body>
</html>"""

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(page.encode("utf-8"))

        except Exception:
            error_html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Dirty Kid Error</title>
  <style>
    body {{
      background: #0b0f14;
      color: #ffffff;
      font-family: Arial, Helvetica, sans-serif;
      padding: 20px;
    }}
    pre {{
      white-space: pre-wrap;
      background: #111821;
      padding: 12px;
      border-radius: 8px;
    }}
  </style>
</head>
<body>
  <h1>Dirty Kid Dashboard Error</h1>
  <pre>{html.escape(traceback.format_exc())}</pre>
</body>
</html>"""
            self.send_response(500)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(error_html.encode("utf-8"))
