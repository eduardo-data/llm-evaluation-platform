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

## Version 2.0 — Model Comparison Mode

Version 2 introduces a benchmarking mode that allows comparing two local LLMs simultaneously and evaluating their responses side by side.

### New Capabilities

- Run multiple models in parallel
- Compare responses visually
- Measure response latency per model
- Calculate metrics for each model independently
- Structured comparison output

### How It Works

Instead of sending a prompt to a single model, the system:

1. Sends the same prompt to Model A and Model B
2. Collects both responses independently
3. Measures response time for each model
4. Calculates evaluation metrics for each output
5. Displays results in a comparison table

This simulates real-world model benchmarking pipelines used in production AI systems.

---

### Example Comparison Output

| Model | Latency | BLEU | ROUGE-L | Similarity |
|------|--------|------|---------|------------|
| mistral | 0.82s | 0.71 | 0.80 | 0.92 |
| phi4-mini | 0.54s | 0.68 | 0.77 | 0.90 |

---

### Why This Matters

Modern AI applications rarely rely on a single model. Production environments frequently compare models to determine:

- response quality
- inference speed
- consistency
- performance tradeoffs

This version demonstrates practical experience with multi-model evaluation pipelines and benchmarking methodologies.

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


git clone https://github.com/eduardo-data/llm-evaluation-platform.git

cd llm-eval-docker


Build containers:


docker compose build


Start services:


docker compose up -d


Download models (first run only):


docker exec -it ollama ollama pull mistral
docker exec -it ollama ollama pull phi4-mini


---

## Usage

Open your browser:


http://localhost:5000


Input:

- Prompt (required)
- Reference answer (optional)
- Model A
- Model B

The system returns:

- Both model responses
- Latency per model
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
- benchmarking multiple models

---

## Future Improvements

- BERTScore metric
- Multi-model batch comparison
- Prompt A/B testing automation
- Experiment tracking dashboard
- Evaluation history logging
- Performance visualization charts

---

## Author

Luiz Eduardo  
Data Scientist  

LinkedIn: https://www.linkedin.com/in/luizeduardodatascientist/  
GitHub: https://github.com/eduardo-data