import json
from pathlib import Path
from typing import List, Dict, Any
import os

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

KB_PATH = Path("data/knowledge_base.json")

EMB_MODEL_NAME = os.getenv("EMB_MODEL_NAME", "all-MiniLM-L6-v2")
_embedder = SentenceTransformer(EMB_MODEL_NAME)

def load_kb() -> List[Dict[str, Any]]:
    if not KB_PATH.exists():
        raise FileNotFoundError(f"Knowledge base not found: {KB_PATH}")
    return json.loads(KB_PATH.read_text(encoding="utf-8"))

def retrieve(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    kb = load_kb()
    q_emb = _embedder.encode(query)

    scored = []
    for doc in kb:
        d_emb = _embedder.encode(doc["text"])
        score = float(cosine_similarity([q_emb], [d_emb])[0][0])
        scored.append({"id": doc["id"], "text": doc["text"], "score": score})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]

def build_context(chunks: List[Dict[str, Any]]) -> str:
    # contexto enxuto e direto
    return "\n".join([f"- {c['text']}" for c in chunks])

def top_ids(chunks: List[Dict[str, Any]]) -> str:
    return ",".join([c["id"] for c in chunks])