from flask import Flask, render_template, request
from llm import ask_llm
from metrics import calculate_all

app = Flask(__name__)

# Modelos sugeridos para comparação
DEFAULT_MODELS = ["mistral", "phi4-mini"]

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        question = (request.form.get("question") or "").strip()
        reference = (request.form.get("reference") or "").strip()

        model_a = request.form.get("model_a") or DEFAULT_MODELS[0]
        model_b = request.form.get("model_b") or DEFAULT_MODELS[1]

        # chama os dois modelos
        a = ask_llm(question, model_a)
        b = ask_llm(question, model_b)

        result = {
            "question": question,
            "reference": reference,
            "models": [
                {
                    "name": model_a,
                    "response": a["text"],
                    "latency_s": round(a["latency_s"], 3),
                    "metrics": calculate_all(reference, a["text"]) if reference else None,
                },
                {
                    "name": model_b,
                    "response": b["text"],
                    "latency_s": round(b["latency_s"], 3),
                    "metrics": calculate_all(reference, b["text"]) if reference else None,
                },
            ],
        }

    return render_template("index.html", result=result, models=DEFAULT_MODELS)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)