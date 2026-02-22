# README DE ESTUDO — LLM Evaluation Platform

Este arquivo é minha documentação pessoal para entender profundamente o projeto.

---

# VISÃO GERAL

Este projeto é um sistema de avaliação de respostas de modelos de linguagem (LLMs) rodando localmente.

Fluxo:

Usuário → Flask → Ollama → Modelo → Métricas → Interface

Ou seja:

1) usuário faz pergunta
2) Flask recebe
3) envia para LLM local
4) recebe resposta
5) calcula métricas
6) mostra resultado

---

# ARQUITETURA

## app/main.py

Função principal do sistema.

Responsabilidades:

- receber pergunta
- chamar LLM
- calcular métricas
- renderizar página HTML

Essa linha roda o servidor:

app.run(host="0.0.0.0", port=5000)

Significa:

aceitar conexões externas (container).

---

## app/llm.py

Responsável por falar com o modelo.

Ele faz POST para:

http://ollama:11434/api/generate

Isso envia prompt para o modelo.

---

## app/metrics.py

Aqui acontece a avaliação.

Temos 3 métricas:

BLEU → similaridade textual exata  
ROUGE → sobreposição de conteúdo  
Cosine → similaridade semântica  

Funções:

bleu() → mede correspondência literal  
rouge_l() → mede subsequência comum  
cosine_sim() → mede similaridade de significado  

---

## templates/index.html

Interface simples.

Recebe input do usuário e mostra:

- resposta
- métricas

---

## Dockerfile

Cria ambiente isolado para rodar projeto.

Passos:

1) usa imagem python
2) instala libs
3) copia código
4) roda servidor

---

## docker-compose.yml

Roda 2 containers:

Container 1 → Ollama (modelo)
Container 2 → Flask (app)

Eles se comunicam pela rede interna Docker.

---

# MÉTRICAS — EXPLICAÇÃO PROFUNDA

BLEU
mede igualdade textual exata
se frase mudar ordem → cai score

ROUGE
mede sobreposição de palavras
mais tolerante

Cosine similarity
mede significado
usa embeddings vetoriais

Regra importante:

BLEU bom → texto igual  
Cosine bom → significado igual  

---

# O QUE DIZER NA ENTREVISTA

Se perguntarem:

"O que esse projeto demonstra?"

Resposta:

Demonstra capacidade de construir pipelines de avaliação de LLM usando métricas automáticas e execução local de modelos.

---

Se perguntarem:

"Por que rodar modelo local?"

Resposta:

Privacidade, custo zero e controle total do ambiente.

---

Se perguntarem:

"Por que usar várias métricas?"

Resposta:

Nenhuma métrica isolada é confiável. Cada uma mede um aspecto diferente da qualidade da resposta.

---

Se perguntarem:

"Qual métrica é melhor?"

Resposta:

Depende da tarefa. Para tradução → BLEU.  
Para resumo → ROUGE.  
Para LLM moderno → Similaridade semântica.

---

Se perguntarem:

"Qual foi o maior desafio?"

Resposta sugerida:

Containerização e integração entre modelo local e pipeline de avaliação.

---

# EXTENSÕES FUTURAS

Ideias para evoluir:

- comparar 2 modelos
- salvar histórico
- ranking automático
- avaliação humana + automática
- dashboard

---

# CONCLUSÃO

Esse projeto prova:

- conhecimento de IA
- engenharia de software
- docker
- NLP
- avaliação de modelos


⭐ Extra — Respostas rápidas de entrevista (cola mental)

Memorize isso:

Este projeto implementa um pipeline completo de avaliação de LLM com execução local, métricas automáticas e arquitetura containerizada.