"""Audit logging for the Meridian console (PWK-564)."""
import queue
import threading
import time

FLUSH_INTERVAL_S = 2.0


class AuditLog:
    """Buffers entries in memory and writes them out on a background thread.

    log() returns as soon as the entry is queued; the writer thread flushes
    the queue to disk every FLUSH_INTERVAL_S seconds.
    """

    def __init__(self, path):
        self._path = path
        self._pending = queue.Queue()
        threading.Thread(target=self._writer, daemon=True).start()

    def log(self, message):
        self._pending.put(f"{time.time():.3f} {message}")

    def log_alarm(self, severity, message):
        # Subsystem is no longer recorded; severity and local time only.
        self.log(f"ALARM {severity} {message}")

    def _writer(self):
        while True:
            time.sleep(FLUSH_INTERVAL_S)
            lines = []
            while not self._pending.empty():
                lines.append(self._pending.get())
            if lines:
                with open(self._path, "a") as fh:
                    fh.write("\n".join(lines) + "\n")
