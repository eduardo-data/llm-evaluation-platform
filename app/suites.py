import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Any, Optional

from llm import ask_llm
from metrics import calculate_all
from prompts import PROMPT_TEMPLATES

SUITES_PATH = Path("data/conversation_suites.json")

@dataclass
class TurnResult:
    turn_index: int
    user: str
    reference: str
    response: str
    latency_s: float
    metrics: Dict[str, Any]

@dataclass
class SuiteRunResult:
    suite_id: str
    suite_name: str
    model: str
    prompt_key: str
    turn_results: List[TurnResult]
    aggregates: Dict[str, Any]

def load_suites() -> List[Dict[str, Any]]:
    if not SUITES_PATH.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {SUITES_PATH}")
    return json.loads(SUITES_PATH.read_text(encoding="utf-8"))

def _build_context(history: List[Dict[str, str]]) -> str:
    """
    Constrói um contexto simples com turns anteriores.
    Isso simula uma jornada conversacional (multi-turn) sem usar API de chat.
    """
    blocks = []
    for msg in history:
        role = msg["role"].upper()
        blocks.append(f"[{role}]\n{msg['content']}")
    return "\n\n".join(blocks)

def run_suite(
    suite: Dict[str, Any],
    model: str,
    prompt_key: str,
    num_predict: int = 128,
) -> SuiteRunResult:
    prompt_cfg = PROMPT_TEMPLATES[prompt_key]

    history: List[Dict[str, str]] = []
    turn_results: List[TurnResult] = []

    for i, turn in enumerate(suite["turns"]):
        user_q = (turn.get("user") or "").strip()
        reference = (turn.get("reference") or "").strip()

        # contexto = histórico + pergunta atual
        context = _build_context(history)
        if context:
            question_with_context = f"{context}\n\n[USER]\n{user_q}"
        else:
            question_with_context = user_q

        # chama LLM com template+system
        llm_out = ask_llm(
            question_with_context,
            model=model,
            system=prompt_cfg["system"],
            template=prompt_cfg["template"],
            num_predict=num_predict,
        )

        response = llm_out["text"]
        latency_s = llm_out["latency_s"]

        metrics = calculate_all(
            question=user_q,
            reference=reference,
            candidate=response,
        )

        turn_results.append(
            TurnResult(
                turn_index=i,
                user=user_q,
                reference=reference,
                response=response,
                latency_s=latency_s,
                metrics=metrics,
            )
        )

        # atualiza histórico (para o próximo turno)
        history.append({"role": "user", "content": user_q})
        history.append({"role": "assistant", "content": response})

    aggregates = aggregate_suite_results(turn_results)

    return SuiteRunResult(
        suite_id=suite["id"],
        suite_name=suite["name"],
        model=model,
        prompt_key=prompt_key,
        turn_results=turn_results,
        aggregates=aggregates,
    )

def aggregate_suite_results(turn_results: List[TurnResult]) -> Dict[str, Any]:
    """
    Agrega médias. Atenção: BLEU/ROUGE/similarity dependem de referência.
    Se reference estiver vazia, eles podem vir None.
    """
    def mean(values: List[float]) -> Optional[float]:
        vals = [v for v in values if v is not None]
        if not vals:
            return None
        return sum(vals) / len(vals)

    bleus = [tr.metrics.get("bleu") for tr in turn_results]
    rouges = [tr.metrics.get("rougeL") for tr in turn_results]
    sims = [tr.metrics.get("similarity") for tr in turn_results]
    precs = [tr.metrics.get("precision") for tr in turn_results]
    rels = [tr.metrics.get("relevance") for tr in turn_results]
    cohs = [tr.metrics.get("coherence") for tr in turn_results]
    lats = [tr.latency_s for tr in turn_results]

    return {
        "avg_latency_s": round(mean(lats) or 0.0, 4),
        "avg_bleu": round(mean(bleus) or 0.0, 4) if mean(bleus) is not None else None,
        "avg_rougeL": round(mean(rouges) or 0.0, 4) if mean(rouges) is not None else None,
        "avg_similarity": round(mean(sims) or 0.0, 4) if mean(sims) is not None else None,
        "avg_precision": round(mean(precs) or 0.0, 4) if mean(precs) is not None else None,
        "avg_relevance": round(mean(rels) or 0.0, 4) if mean(rels) is not None else None,
        "avg_coherence": round(mean(cohs) or 0.0, 4) if mean(cohs) is not None else None,
        "turns": len(turn_results),
    }