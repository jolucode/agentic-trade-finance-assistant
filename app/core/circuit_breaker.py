import time


class CircuitBreaker:

    def __init__(
        self,
        failure_threshold: int = 3,
        recovery_timeout: int = 10
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout

        self.failure_count = 0
        self.state = "CLOSED"
        self.opened_at = None

    def can_execute(self) -> bool:

        if self.state == "CLOSED":
            return True

        if self.state == "OPEN":

            elapsed = time.time() - self.opened_at

            if elapsed >= self.recovery_timeout:
                self.state = "HALF_OPEN"
                return True

            return False

        if self.state == "HALF_OPEN":
            return True

        return False

    def record_success(self):

        self.failure_count = 0
        self.state = "CLOSED"
        self.opened_at = None

    def record_failure(self):

        self.failure_count += 1

        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            self.opened_at = time.time()