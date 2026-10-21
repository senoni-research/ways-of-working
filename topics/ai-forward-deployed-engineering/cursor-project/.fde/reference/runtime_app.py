"""An agent served the way AgentCore Runtime's HTTP contract asks, without a web framework: POST /invocations does
the work and GET /ping reports Healthy, or HealthyBusy while background work runs. Standard library only.

Two documented traps are built in as controls. time_of_last_update moves only when the status changes: if it moved on
every ping, the session would never go idle and would run to its maximum lifetime. And nothing random, unique, timed
or credentialed is made at startup, because instances restored from one snapshot share whatever startup made.
"""
from __future__ import annotations

import secrets
import time


class Agent:
    def __init__(self, decide, clock=time.time):
        self.decide, self.clock = decide, clock
        self.config = {'model': 'stub', 'tools': ('read_claim', 'decide')}
        self.tasks: set[str] = set()
        self.status, self.changed = 'Healthy', int(clock())

    def handle(self, method: str, path: str, body: dict | None = None) -> tuple[int, dict]:
        if (method, path) == ('GET', '/ping'):
            return 200, self.ping()
        if (method, path) == ('POST', '/invocations'):
            return 200, {'request_id': secrets.token_hex(16), **self.decide(body)}
        return 404, {'error': 'not found'}

    def ping(self) -> dict:
        status = 'HealthyBusy' if self.tasks else 'Healthy'
        if status != self.status:
            self.status, self.changed = status, int(self.clock())
        return {'status': status, 'time_of_last_update': self.changed}

    def start_task(self) -> str:
        task = secrets.token_hex(8)
        self.tasks.add(task)
        return task

    def finish_task(self, task: str):
        self.tasks.discard(task)

    def jitter(self, base: float) -> float:
        """A retry delay drawn from the operating system per call, so restored instances don't retry in step."""
        return secrets.SystemRandom().random() * base
