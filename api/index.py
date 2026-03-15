import json
import traceback
from http.server import BaseHTTPRequestHandler
from dirtykid_agent import run_dirty_kid


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            result = run_dirty_kid()

            price = result["snapshot"]["price"]
            signal = result["execution"]["action"]
            reason = result["execution"]["reason"]
            reasons = "<br>".join(result["analysis"]["reasons"])

            html = f"""
            <html>
            <head>
            <title>Dirty Kid Agent</title>
            <style>
            body {{
                background:#0b0f14;
                color:#00ff9d;
                font-family:monospace;
                text-align:center;
                padding:40px;
            }}
            .card {{
                background:#111821;
                border-radius:12px;
                padding:30px;
                width:350px;
                margin:auto;
                box-shadow:0 0 20px rgba(0,255,150,0.15);
            }}
            .title {{
                font-size:28px;
                margin-bottom:20px;
            }}
            .price {{
                font-size:32px;
                margin-bottom:10px;
            }}
            .signal {{
                font-size:26px;
                margin:15px 0;
            }}
            .reason {{
                color:#9fb3c8;
                font-size:14px;
            }}
            </style>
            </head>

            <body>

            <div class="card">
                <div class="title">DIRTY KID AGENT</div>

                <div class="price">BTC ${price:,.2f}</div>

                <div class="signal">Signal: {signal}</div>

                <div class="reason">{reason}</div>

                <br>

                <div class="reason">{reasons}</div>
            </div>

            </body>
            </html>
            """

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())

        except Exception as e:

            error = {
                "error": str(e),
                "traceback": traceback.format_exc()
            }

            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(error).encode())
