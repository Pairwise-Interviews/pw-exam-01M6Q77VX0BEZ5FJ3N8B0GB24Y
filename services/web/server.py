"""Stub web. GET / is a static HTML page that says this is a stub; every other path is 404 (C3.M5)."""

import os
import signal
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PAGE = b"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Stub web</title></head>
<body><h1>Stub web</h1><p>This is the kit's stub. Replace it with a page that shows each job's state.</p></body></html>
"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, content_type: str, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            self._send(200, "text/html; charset=utf-8", PAGE)
        else:
            self._send(404, "text/plain; charset=utf-8", b"not found\n")

    def log_message(self, fmt, *args):
        pass


def main() -> None:
    server = ThreadingHTTPServer(("0.0.0.0", int(os.environ.get("PORT", "3000"))), Handler)
    server.daemon_threads = True
    signal.signal(signal.SIGTERM, lambda *_: threading.Thread(target=server.shutdown).start())
    server.serve_forever()


if __name__ == "__main__":
    main()
