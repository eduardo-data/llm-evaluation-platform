![demo](docs/demo.gif)

# LLM Evaluation Platform (Local LLM + Metrics)

This project implements a complete evaluation and benchmarking pipeline for Large Language Models running locally using Ollama. It provides a web interface where users can submit prompts, receive model responses, compare outputs, and evaluate quality using multiple NLP metrics.

---

## Overview

The system runs local LLMs, sends prompts through a Flask API, evaluates generated outputs, logs results, and displays metrics in real time.

It simulates real-world AI validation workflows used in production environments.

Architecture flow:

Browser → Flask App → Ollama API → Local LLM → Metrics Engine → Storage → Dashboard UI

---

## Core Features

- Local LLM execution (no external APIs required)
- Multi-model comparison (A/B testing)
- Automated evaluation metrics
- Prompt template system
- Conversation test suites (multi-turn testing)
- Evaluation logging + monitoring
- Fully containerized environment
- Reproducible setup using Docker

---

# Version 2.0 — Model Comparison Mode

Version 2 introduced a benchmarking mode that allows comparing two local LLMs simultaneously and evaluating responses side by side.

### Capabilities

- Run multiple models in parallel
- Compare responses visually
- Measure response latency per model
- Calculate metrics per output
- Structured comparison table

---

### How It Works

Instead of sending a prompt to a single model, the system:

1. Sends the same prompt to Model A and Model B
2. Collects both responses independently
3. Measures latency
4. Calculates evaluation metrics
5. Displays comparison results

This simulates real-world model benchmarking pipelines used in production AI systems.

---

### Example Output

| Model | Latency | BLEU | ROUGE-L | Similarity |
|------|--------|------|---------|------------|
| mistral | 0.82s | 0.71 | 0.80 | 0.92 |
| phi4-mini | 0.54s | 0.68 | 0.77 | 0.90 |

---

# Version 3.0 — Conversational Evaluation & Monitoring

Version 3 expands the system into a complete evaluation platform with conversation test suites, logging, and monitoring.

### New Capabilities

- Multi-turn conversation testing
- Regression testing for prompts/models
- Automated suite execution
- Aggregated metrics per test suite
- SQLite experiment logging
- Performance monitoring dashboard
- Human evaluation signals (correctness, relevance, coherence)

---

### Why This Matters

Production AI systems must be tested across realistic conversations, not isolated prompts.

This version demonstrates experience with:

- conversational testing
- regression evaluation
- monitoring pipelines
- evaluation reproducibility

---

### Conversation Test Suites

Suites simulate real chat interactions with sequential turns and expected answers.

Each suite run produces:

- response per turn
- latency per turn
- metrics per turn
- aggregated metrics

This mirrors testing pipelines used in real conversational AI deployments.

---

## Metrics Implemented

### BLEU
Measures exact token overlap between generated output and reference text. Best suited for strict textual similarity tasks.

### ROUGE-L
Measures the longest common subsequence between texts. Useful for content similarity and summarization evaluation.

### Semantic Similarity (Cosine Similarity)
Uses embeddings to compare semantic meaning rather than exact wording.

### Additional Evaluation Signals

- Precision (semantic correctness proxy)
- Relevance (question–answer alignment)
- Coherence (text quality heuristic)

These approximate real evaluation signals used in LLM quality pipelines.

---

## Requirements

- Docker
- Docker Compose

---

## Installation

Clone repository:

```
git clone https://github.com/eduardo-data/llm-evaluation-platform.git
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

Download models (first run only):

```
docker exec -it ollama ollama pull mistral
docker exec -it ollama ollama pull phi4-mini
```

---

## Usage

Open:

```
http://localhost:5000
```

Suite runner:

```
http://localhost:5000/suites
```

---

## Use Cases

This project simulates real-world LLM validation workflows used for:

- AI response quality analysis
- Prompt engineering testing
- Conversational AI evaluation
- Model benchmarking
- Regression testing
- Monitoring model behavior
- Retrieval-Augmented Generation validation

---

## Tech Stack

- Python
- Flask
- Ollama
- Sentence Transformers
- Scikit-learn
- SQLite
- Docker

---

## Architecture Highlights

This project demonstrates hands-on experience with:

- local LLM orchestration
- prompt engineering systems
- evaluation pipelines
- experiment logging
- monitoring
- A/B testing
- conversational testing
- reproducible environments

---

## Why This Project Matters

Modern AI systems require automated pipelines to validate output quality, consistency, and reliability.

This project demonstrates practical experience with:

- running local LLMs
- integrating model APIs
- evaluating generated outputs
- building testing pipelines
- containerizing applications
- benchmarking multiple models
- monitoring model behavior

---

## Future Improvements

- BERTScore metric
- multi-model batch benchmarking
- automated prompt optimization
- experiment tracking UI
- performance visualization charts
- distributed evaluation workers

---

## Author

Luiz Eduardo  
Data Scientist  

LinkedIn: https://www.linkedin.com/in/luizeduardodatascientist/  
GitHub: https://github.com/eduardo-data