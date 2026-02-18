from sentence_transformers import SentenceTransformer, util
import numpy as np

class IntentRouter:
    def __init__(self):
        # lightweight embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        # define canonical prompts per mode
        self.modes = {
            "strategic": "business strategy market analysis startup plan financial projection",
            "research": "evaluate reliability reproducibility dataset metrics experiment",
            "simulation": "simulate scenario forecast alternative futures monte carlo policy impact",
            "governance": "compliance security audit policy risk control"
        }
        # precompute mode embeddings
        self.mode_embeddings = {}
        texts = list(self.modes.values())
        embeddings = self.model.encode(texts, convert_to_tensor=True)
        for k, emb in zip(self.modes.keys(), embeddings):
            self.mode_embeddings[k] = emb

    def classify(self, text: str) -> str:
        emb = self.model.encode(text, convert_to_tensor=True)
        best_mode = None
        best_score = -1.0
        for mode, mode_emb in self.mode_embeddings.items():
            score = util.cos_sim(emb, mode_emb).item()
            if score > best_score:
                best_score = score
                best_mode = mode
        return best_mode
