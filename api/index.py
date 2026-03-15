from http.server import BaseHTTPRequestHandler
import json
from dirtykid_agent import run_dirty_kid


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        result = run_dirty_kid()

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        response = {
            "status": "ok",
            "post": result["post"],
            "snapshot": result["snapshot"],
            "analysis": result["analysis"],
            "risk": result["risk"],
            "execution": result["execution"],
        }

        self.wfile.write(json.dumps(response).encode())
        return
