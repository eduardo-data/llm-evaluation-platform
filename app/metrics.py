import os
import re
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

EMB_MODEL_NAME = os.getenv("EMB_MODEL_NAME", "all-MiniLM-L6-v2")
_embedder = SentenceTransformer(EMB_MODEL_NAME)

_rouge = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
_smooth = SmoothingFunction().method1

def bleu(reference: str, candidate: str) -> float:
    ref_tokens = reference.split()
    cand_tokens = candidate.split()
    return float(sentence_bleu([ref_tokens], cand_tokens, smoothing_function=_smooth))

def rouge_l(reference: str, candidate: str) -> float:
    scores = _rouge.score(reference, candidate)
    return float(scores["rougeL"].fmeasure)

def semantic_similarity(a: str, b: str) -> float:
    e1 = _embedder.encode(a)
    e2 = _embedder.encode(b)
    return float(cosine_similarity([e1], [e2])[0][0])

def precision_semantic(reference: str, candidate: str) -> float:
    if not reference.strip():
        return 0.0
    return semantic_similarity(reference, candidate)

def relevance(question: str, candidate: str) -> float:
    return semantic_similarity(question, candidate)

def coherence(candidate: str) -> float:
    text = candidate.strip()
    if len(text) < 20:
        return 0.2
    non_text_ratio = len(re.findall(r"[^a-zA-ZÀ-ÿ0-9\s\.,;:!\?\-\(\)]", text)) / max(len(text), 1)
    score = 1.0 - min(non_text_ratio * 3.0, 0.6)
    if text.count(".") + text.count("!") + text.count("?") >= 1:
        score += 0.1
    return max(0.0, min(1.0, score))

def calculate_all(question: str, reference: str, candidate: str) -> dict:
    return {
        "bleu": round(bleu(reference, candidate), 4) if reference else None,
        "rougeL": round(rouge_l(reference, candidate), 4) if reference else None,
        "similarity": round(semantic_similarity(reference, candidate), 4) if reference else None,
        "precision": round(precision_semantic(reference, candidate), 4) if reference else None,
        "relevance": round(relevance(question, candidate), 4),
        "coherence": round(coherence(candidate), 4),
    }