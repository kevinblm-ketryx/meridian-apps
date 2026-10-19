"""Service menu session handling for the Meridian console (PWK-567)."""
import time

# Lock the service menu after this many seconds without input.
SERVICE_IDLE_TIMEOUT_S = 10 * 60


class ServiceSession:
    def __init__(self, clock=time.monotonic):
        self._clock = clock
        self._last_input = clock()
        self.locked = False

    def touch(self):
        """Record operator input and keep the session open."""
        if not self.locked:
            self._last_input = self._clock()

    def check_idle(self):
        """Lock the session once it has been idle past the timeout."""
        if self._clock() - self._last_input >= SERVICE_IDLE_TIMEOUT_S:
            self.locked = True
        return self.locked

    def unlock(self, credential_ok):
        """Re-open a locked session only after the credential is re-entered."""
        if credential_ok:
            self.locked = False
            self._last_input = self._clock()
        return not self.locked
