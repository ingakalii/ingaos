import os
from rq import Queue
from redis import Redis
import json

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_conn = Redis.from_url(redis_url)
q = Queue("default", connection=redis_conn, default_timeout=600)

class Orchestrator:
    def __init__(self):
        self.queue = q

    def run(self, mode: str, payload: dict) -> str:
        # For demo we push a simple job; in real system jobs map to worker functions
        job = self.queue.enqueue("app.agents.task_worker.handle_task", mode, payload, result_ttl=3600)
        return job.get_id()
