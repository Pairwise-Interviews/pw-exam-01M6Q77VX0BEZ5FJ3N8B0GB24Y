"""Stub api. GET /healthz is 200 only when Postgres answers SELECT 1 at DATABASE_URL; every other path is 404.

Replace this with your own api (C3.M5). It stops on SIGTERM at once, so a stop does not wait for the stop grace.
"""

import os
import signal
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import psycopg


def database_ok() -> bool:
    try:
        with psycopg.connect(os.environ["DATABASE_URL"], connect_timeout=2) as conn:
            return conn.execute("SELECT 1").fetchone() == (1,)
    except Exception:
        return False


class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, body: bytes = b"") -> None:
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _route(self) -> None:
        if self.command == "GET" and self.path == "/healthz":
            ok = database_ok()
            self._send(200 if ok else 503, b"ok\n" if ok else b"postgres unreachable\n")
        else:
            self._send(404, b"not found\n")

    do_GET = do_POST = do_PUT = do_DELETE = _route

    def log_message(self, fmt, *args):
        pass


def main() -> None:
    server = ThreadingHTTPServer(("0.0.0.0", int(os.environ.get("PORT", "8000"))), Handler)
    server.daemon_threads = True
    # shutdown() blocks until serve_forever() returns, so it cannot run in the signal handler's own thread.
    signal.signal(signal.SIGTERM, lambda *_: threading.Thread(target=server.shutdown).start())
    server.serve_forever()


if __name__ == "__main__":
    main()
