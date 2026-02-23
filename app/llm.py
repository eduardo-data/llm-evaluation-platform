import os
import time
import requests

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")

def ask_llm(
    question: str,
    model: str,
    system: str = "",
    template: str = "{question}",
    num_predict: int = 128
) -> dict:
    prompt = template.format(question=question).strip()
    if system:
        # "system prompt" simples (embutido)
        prompt = f"[SYSTEM]\n{system}\n\n[USER]\n{prompt}"

    url = f"{OLLAMA_HOST}/api/generate"
    t0 = time.perf_counter()

    r = requests.post(
        url,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"num_predict": num_predict},
        },
        timeout=180,
    )
    r.raise_for_status()

    latency = time.perf_counter() - t0
    data = r.json()

    return {
        "text": (data.get("response") or "").strip(),
        "latency_s": latency,
        "prompt_used": prompt
    }