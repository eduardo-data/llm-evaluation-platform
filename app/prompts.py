PROMPT_TEMPLATES = {
    "direct": {
        "name": "Direct Answer",
        "system": "Você é um assistente objetivo e preciso. Responda de forma curta.",
        "template": "{question}"
    },
    "reasoned": {
        "name": "Reasoned + Structured",
        "system": "Você é um especialista. Responda com explicação curta e depois uma resposta final.",
        "template": "Pergunta: {question}\nResponda com:\n1) Explicação (2-4 linhas)\n2) Resposta final (1 linha)"
    },
}