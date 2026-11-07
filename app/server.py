"""Small standard-library HTTP panel for the isolated local lab."""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from app.database import fixed_search, initialize, vulnerable_search


DATABASE_PATH = os.environ.get(
    "DATABASE_PATH", str(Path(__file__).resolve().parents[1] / "data" / "lab.sqlite3")
)
initialize(DATABASE_PATH)


class Handler(BaseHTTPRequestHandler):
    def respond(self, status, payload, content_type="application/json; charset=utf-8"):
        body = payload.encode("utf-8") if isinstance(payload, str) else json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self.respond(200, "<h1>Rede Vila Aurora — laboratório local</h1><p>Somente dados fictícios. Rotas: /access-history/vulnerable?q=... e /access-history/fixed?q=...</p>", "text/html; charset=utf-8")
            return
        if parsed.path == "/health":
            self.respond(200, {"status": "ok", "data": "synthetic"})
            return
        routes = {
            "/access-history/vulnerable": vulnerable_search,
            "/access-history/fixed": fixed_search,
        }
        search = routes.get(parsed.path)
        if search:
            query = parse_qs(parsed.query).get("q", [""])[0]
            try:
                self.respond(200, {"results": search(query, DATABASE_PATH)})
            except Exception:
                self.respond(400, {"error": "consulta inválida"})
            return
        self.respond(404, {"error": "não encontrado"})

    def log_message(self, format_string, *args):
        print(json.dumps({"source": "web_panel", "message": format_string % args}), flush=True)


if __name__ == "__main__":
    server = ThreadingHTTPServer((os.environ.get("APP_HOST", "127.0.0.1"), int(os.environ.get("APP_PORT", "8080"))), Handler)
    print("Lab panel listening", flush=True)
    server.serve_forever()
