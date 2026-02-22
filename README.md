![demo](docs/demo.gif)
# LLM Evaluation Platform (Local LLM + Metrics)

This project implements a complete evaluation pipeline for Large Language Models running locally using Ollama. It provides a web interface where users can submit prompts, receive model responses, and evaluate output quality using multiple NLP metrics.

---

## Overview

The system runs a local LLM instance, sends prompts through a Flask API, and evaluates the generated output using standard NLP metrics. It simulates a real-world AI evaluation workflow used in production environments.

Architecture flow:

Browser → Flask App → Ollama API → Local LLM → Metrics Engine → Results UI

---

## Features

- Local LLM execution (no external API required)
- Interactive web interface for prompt testing
- Automated evaluation metrics
- Fully containerized environment
- Reproducible setup using Docker
- Realistic AI evaluation pipeline

---

## Metrics Implemented

### BLEU
Measures exact token overlap between generated output and reference text. Best suited for strict textual similarity tasks such as translation.

### ROUGE-L
Measures the longest common subsequence between texts. Useful for evaluating content similarity and summarization tasks.

### Semantic Similarity (Cosine Similarity)
Uses sentence embeddings to compare semantic meaning rather than exact wording. More suitable for modern LLM evaluation.

---

## Requirements

- Docker
- Docker Compose

---

## Installation

Clone repository:

```
git clone <your-repo-url>
cd llm-eval-docker
```

Build containers:

```
docker compose build
```

Start services:

```
docker compose up -d
```

Download model (first run only):

```
docker exec -it ollama ollama pull mistral
```

---

## Usage

Open your browser:

```
http://localhost:5000
```

Input:

- Prompt (required)
- Reference answer (optional)

The system returns:

- Model response
- BLEU score
- ROUGE-L score
- Semantic similarity score

---

## Use Cases

This project simulates real-world LLM validation pipelines used for:

- AI response quality analysis
- Prompt engineering testing
- Conversational AI evaluation
- Model benchmarking
- Retrieval-Augmented Generation validation

---

## Tech Stack

- Python
- Flask
- Ollama
- Sentence Transformers
- Scikit-learn
- Docker

---

## Why This Project Matters

Modern AI systems require automated evaluation pipelines to validate output quality and consistency. This project demonstrates practical experience with:

- running local LLMs
- integrating model APIs
- evaluating generated outputs
- building testing pipelines
- containerizing applications

---

## Future Improvements

- BERTScore metric
- Multi-model comparison
- Prompt A/B testing
- Experiment tracking dashboard
- Evaluation history logging

---

## Author

Luiz Eduardo