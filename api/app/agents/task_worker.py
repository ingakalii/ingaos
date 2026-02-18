# RQ worker module entrypoint for tasks enqueued by orchestrator
from .strategic.market_analyst import MarketAnalyst
from ..infra.qdrant_client import QdrantClient
import os

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
qdrant = QdrantClient(QDRANT_URL)

def handle_task(mode, payload):
    if mode == "strategic":
        agent = MarketAnalyst(qdrant)
        return agent.analyze(payload.get("user_id"), payload.get("text"))
    # expand to other modes
    return {"error": "mode not implemented"}
