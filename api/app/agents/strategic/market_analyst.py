"""
A small, deterministic Market Analyst 'agent' used for the demo.
It uses embeddings to lookup related docs in Qdrant and synthesizes a templated response.
Replace synthesis with a local LLM adapter later.
"""
from ...models.embedding import EmbeddingModel
import uuid

class MarketAnalyst:
    def __init__(self, qdrant_client):
        self.qdrant = qdrant_client
        self.embedder = EmbeddingModel()
        self.collection = "market_docs"
        # ensure collection exists (vector size of all-MiniLM-L6-v2 is 384)
        try:
            self.qdrant.create_collection_if_not_exists(self.collection, 384)
        except Exception:
            pass

    def analyze(self, user_id: str, prompt: str) -> dict:
        # 1) embed query
        qvec = self.embedder.embed(prompt)

        # 2) fetch related docs
        hits = []
        try:
            hits = self.qdrant.search(self.collection, qvec, top_k=5)
        except Exception:
            hits = []

        sources = [h.payload for h in hits] if hits else []

        # 3) simple heuristic "analysis" as template
        # identify simple keywords for demo
        keywords = {"growth": 0, "market": 0, "revenue": 0, "cost": 0, "competitor": 0}
        for k in keywords.keys():
            if k in prompt.lower():
                keywords[k] = 1

        analysis = {
            "summary": f"Quick market analysis for input: '{prompt[:200]}'",
            "high_level_findings": [
                "Market shows potential in niche segments." if keywords["growth"] or keywords["market"] else "Need more market data.",
                "Revenue model requires validation." if keywords["revenue"] else "Revenue assumptions not provided.",
                "Costs should be modeled; watch burn rate." if keywords["cost"] else "Cost data missing.",
            ],
            "recommended_next_steps": [
                "Collect TAM/SAM figures and store in memory.",
                "Run unit-economics calculator (burn & runway).",
                "Run competitor analysis using web scrapes into vector DB."
            ],
            "evidence": sources,
            "meta": {
                "id": str(uuid.uuid4()),
                "confidence_score": 0.42  # placeholder: real system computes this
            }
        }
        return analysis
