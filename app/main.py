from flask import Flask, render_template, request
from llm import ask_llm
from metrics import calculate_all

app = Flask(__name__)

@app.get("/")
def home():
    return render_template("index.html", result=None)

@app.post("/")
def ask():
    question = request.form.get("question", "").strip()
    reference = request.form.get("reference", "").strip()

    if not question:
        return render_template("index.html", result={"error": "Digite uma pergunta."})

    response = ask_llm(question)

    result = {
        "question": question,
        "reference": reference,
        "response": response,
    }

    if reference:
        result["metrics"] = calculate_all(reference, response)
    else:
        result["metrics"] = None

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)