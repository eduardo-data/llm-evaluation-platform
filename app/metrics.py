import os
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Cache do modelo (vamos apontar isso no Dockerfile)
EMB_MODEL_NAME = os.getenv("EMB_MODEL_NAME", "all-MiniLM-L6-v2")
_embedder = SentenceTransformer(EMB_MODEL_NAME)

_rouge = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
_smooth = SmoothingFunction().method1

def bleu(reference: str, candidate: str) -> float:
    # BLEU em frases curtas pode dar 0 sem smoothing
    ref_tokens = reference.split()
    cand_tokens = candidate.split()
    return float(sentence_bleu([ref_tokens], cand_tokens, smoothing_function=_smooth))

def rouge_l(reference: str, candidate: str) -> float:
    scores = _rouge.score(reference, candidate)
    return float(scores["rougeL"].fmeasure)

def semantic_similarity(reference: str, candidate: str) -> float:
    e1 = _embedder.encode(reference)
    e2 = _embedder.encode(candidate)
    return float(cosine_similarity([e1], [e2])[0][0])

def calculate_all(reference: str, candidate: str) -> dict:
    return {
        "bleu": round(bleu(reference, candidate), 4),
        "rougeL": round(rouge_l(reference, candidate), 4),
        "similarity": round(semantic_similarity(reference, candidate), 4),
    }