import os
import requests

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

def ask_llm(prompt: str) -> str:
    url = f"{OLLAMA_HOST}/api/generate"
    r = requests.post(
        url,
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
        timeout=120,
    )
    r.raise_for_status()
    data = r.json()
    return (data.get("response") or "").strip()