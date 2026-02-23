import os
import sqlite3
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "/app/data/evals.db")

def _conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    with _conn() as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS eval_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT,
            question TEXT,
            reference TEXT,
            model TEXT,
            prompt_name TEXT,
            prompt_used TEXT,
            response TEXT,
            latency_s REAL,

            rag_used INTEGER,
            rag_top_ids TEXT,

            bleu REAL,
            rougeL REAL,
            similarity REAL,
            precision REAL,
            relevance REAL,
            coherence REAL,

            human_correct INTEGER,
            human_relevant INTEGER,
            human_coherent INTEGER
        )
        """)
        con.commit()

def log_run(payload: dict):
    with _conn() as con:
        con.execute("""
        INSERT INTO eval_runs (
            created_at, question, reference, model, prompt_name, prompt_used, response, latency_s,
            rag_used, rag_top_ids,
            bleu, rougeL, similarity, precision, relevance, coherence,
            human_correct, human_relevant, human_coherent
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.utcnow().isoformat(),
            payload.get("question"),
            payload.get("reference"),
            payload.get("model"),
            payload.get("prompt_name"),
            payload.get("prompt_used"),
            payload.get("response"),
            payload.get("latency_s"),

            payload.get("rag_used", 0),
            payload.get("rag_top_ids", ""),

            payload.get("bleu"),
            payload.get("rougeL"),
            payload.get("similarity"),
            payload.get("precision"),
            payload.get("relevance"),
            payload.get("coherence"),

            payload.get("human_correct", 0),
            payload.get("human_relevant", 0),
            payload.get("human_coherent", 0),
        ))
        con.commit()

def get_dashboard_stats(limit: int = 200):
    with _conn() as con:
        rows = con.execute("""
        SELECT model, prompt_name,
               COUNT(*) as n,
               AVG(latency_s) as avg_latency,
               AVG(COALESCE(bleu, 0)) as avg_bleu,
               AVG(COALESCE(rougeL, 0)) as avg_rougeL,
               AVG(COALESCE(similarity, 0)) as avg_similarity,
               AVG(COALESCE(relevance, 0)) as avg_relevance,
               AVG(COALESCE(coherence, 0)) as avg_coherence,
               AVG(COALESCE(human_correct, 0)) as avg_human_correct,
               AVG(COALESCE(rag_used, 0)) as avg_rag_used
        FROM eval_runs
        GROUP BY model, prompt_name
        ORDER BY n DESC
        """).fetchall()

        recent = con.execute("""
        SELECT created_at, model, prompt_name, latency_s, relevance, coherence, human_correct, rag_used, rag_top_ids
        FROM eval_runs
        ORDER BY id DESC
        LIMIT ?
        """, (limit,)).fetchall()

    return rows, recent