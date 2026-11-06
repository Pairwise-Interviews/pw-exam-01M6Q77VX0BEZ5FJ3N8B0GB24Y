"""Stub worker. It opens no port and waits for SIGTERM (C3.M5)."""

import signal
import threading

stop = threading.Event()
signal.signal(signal.SIGTERM, lambda *_: stop.set())
signal.signal(signal.SIGINT, lambda *_: stop.set())
stop.wait()
