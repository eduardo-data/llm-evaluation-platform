from flask import Flask, render_template, request
from llm import ask_llm
from metrics import calculate_all
from prompts import PROMPT_TEMPLATES
from storage import init_db, log_run, get_dashboard_stats
from rag import retrieve, build_context, top_ids

app = Flask(__name__)
init_db()

DEFAULT_MODELS = ["mistral", "phi4-mini"]

@app.get("/")
def home():
    return render_template(
        "index.html",
        result=None,
        models=DEFAULT_MODELS,
        prompts=PROMPT_TEMPLATES
    )

@app.post("/")
def evaluate():
    question = (request.form.get("question") or "").strip()
    reference = (request.form.get("reference") or "").strip()

    model_a = request.form.get("model_a") or DEFAULT_MODELS[0]
    model_b = request.form.get("model_b") or DEFAULT_MODELS[1]
    prompt_key = request.form.get("prompt_key") or "direct"
    prompt_cfg = PROMPT_TEMPLATES[prompt_key]

    # avaliação humana (checkbox)
    human_correct = 1 if request.form.get("human_correct") == "on" else 0
    human_relevant = 1 if request.form.get("human_relevant") == "on" else 0
    human_coherent = 1 if request.form.get("human_coherent") == "on" else 0

    # RAG opcional
    use_rag = 1 if request.form.get("use_rag") == "on" else 0
    rag_ctx = ""
    rag_ids = ""

    question_for_llm = question
    if use_rag:
        chunks = retrieve(question, top_k=3)
        rag_ctx = build_context(chunks)
        rag_ids = top_ids(chunks)

        question_for_llm = (
            "Use APENAS o contexto abaixo para responder.\n"
            "Se o contexto não for suficiente, diga: \"Não encontrei essa informação no contexto.\"\n\n"
            f"Contexto:\n{rag_ctx}\n\n"
            f"Pergunta:\n{question}"
        )

    # chama LLMs
    a = ask_llm(question_for_llm, model_a, system=prompt_cfg["system"], template=prompt_cfg["template"])
    b = ask_llm(question_for_llm, model_b, system=prompt_cfg["system"], template=prompt_cfg["template"])

    a_metrics = calculate_all(question, reference, a["text"])
    b_metrics = calculate_all(question, reference, b["text"])

    # log no banco
    log_run({
        "question": question,
        "reference": reference,
        "model": model_a,
        "prompt_name": prompt_cfg["name"],
        "prompt_used": a["prompt_used"],
        "response": a["text"],
        "latency_s": a["latency_s"],
        "rag_used": use_rag,
        "rag_top_ids": rag_ids,
        **a_metrics,
        "human_correct": human_correct,
        "human_relevant": human_relevant,
        "human_coherent": human_coherent,
    })

    log_run({
        "question": question,
        "reference": reference,
        "model": model_b,
        "prompt_name": prompt_cfg["name"],
        "prompt_used": b["prompt_used"],
        "response": b["text"],
        "latency_s": b["latency_s"],
        "rag_used": use_rag,
        "rag_top_ids": rag_ids,
        **b_metrics,
        "human_correct": human_correct,
        "human_relevant": human_relevant,
        "human_coherent": human_coherent,
    })

    result = {
        "question": question,
        "reference": reference,
        "prompt_key": prompt_key,
        "use_rag": bool(use_rag),
        "rag_top_ids": rag_ids,
        "models": [
            {"name": model_a, "response": a["text"], "latency_s": round(a["latency_s"], 3), "metrics": a_metrics},
            {"name": model_b, "response": b["text"], "latency_s": round(b["latency_s"], 3), "metrics": b_metrics},
        ],
    }

    return render_template(
        "index.html",
        result=result,
        models=DEFAULT_MODELS,
        prompts=PROMPT_TEMPLATES
    )

@app.get("/dashboard")
def dashboard():
    stats, recent = get_dashboard_stats()
    return render_template("dashboard.html", stats=stats, recent=recent)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)