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



## EXPLICAÇÃO

1) Contexto: o que você está avaliando aqui

Você tem dois textos:

reference: a “resposta esperada” (ground truth), escrita por humano ou por um padrão desejado.

candidate: a “resposta gerada” pelo LLM.

Seu pipeline calcula 3 coisas diferentes:

BLEU → similaridade literal (palavra/trecho)

ROUGE-L → sobreposição de conteúdo via subsequência

Similaridade semântica (cosseno com embeddings) → similaridade de significado

Por que 3 métricas?
Porque cada uma mede um aspecto diferente e nenhuma, sozinha, é “verdade absoluta” em LLM.

2) BLEU (Bilingual Evaluation Understudy)
O que é

BLEU é uma métrica clássica de NLP para avaliar texto gerado comparando com uma referência, muito usada em tradução automática.

Ela mede quanto da sequência de palavras do candidato aparece na referência (n-grams).
Ou seja, quanto o texto é “parecido” na forma.

Intuição

Se o candidato usa as mesmas palavras e em ordem parecida, BLEU sobe.

Se o candidato expressa a mesma ideia, mas com sinônimos/ordem diferente, BLEU pode cair.

Intervalo e interpretação

Geralmente entre 0 e 1 (em implementações comuns).

1.0 = match perfeito (muito raro fora de tarefas “exatas”).

0.0 = pouca ou nenhuma sobreposição literal.

Limitações importantes (isso é ótimo citar na entrevista)

Ruim para referência curta (ex.: referência “Recife”). Mesmo resposta correta “A capital é Recife” pode dar BLEU baixo.

Penaliza paráfrases: “Brasília é a capital” vs “A capital do Brasil é Brasília” pode reduzir BLEU.

Para chat/QA aberto, BLEU costuma não refletir bem qualidade real.

Por que seu código usa “smoothing”

Em frases curtas, BLEU pode virar 0 porque alguns n-grams não aparecem (problema clássico).
O smoothing “suaviza” o cálculo para não zerar tão fácil.

Resposta pronta de entrevista (BLEU)

BLEU mede similaridade textual baseada em n-grams, sendo útil quando se espera uma redação próxima da referência (ex.: tradução). Em respostas abertas, pode ser injusto com paráfrases e referências curtas; por isso uso smoothing e interpreto junto com outras métricas.

3) ROUGE-L (Recall-Oriented Understudy for Gisting Evaluation)
O que é

ROUGE é uma família de métricas muito usada em resumo automático.
O ROUGE-L mede a Longest Common Subsequence (LCS) — a “maior subsequência comum” entre referência e candidato.

Importante:

Subsequência não precisa ser contígua, mas respeita a ordem.

Isso torna ROUGE-L um pouco mais flexível do que BLEU.

Intuição

Se a resposta do modelo contém a mesma informação na mesma ordem geral, ROUGE-L tende a ser maior.

Intervalo e interpretação

Também costuma ficar entre 0 e 1.

1.0 = altamente similar.

Valores intermediários = há sobreposição parcial.

Limitações

Ainda é uma métrica baseada em texto, não em significado.

Sinônimos e reescritas podem reduzir ROUGE.

Se a referência for muito curta, ROUGE-L também pode ficar baixo (embora geralmente menos “cruel” que BLEU).

Resposta pronta de entrevista (ROUGE-L)

ROUGE-L mede similaridade pela maior subsequência comum, sendo comum para avaliar resumos e sobreposição de conteúdo. É mais flexível que BLEU, mas ainda depende de correspondência textual, então complementamos com métricas semânticas.

4) Similaridade semântica com embeddings + cosseno
O que é

Aqui você usa um modelo de embeddings (Sentence Transformers) para transformar cada texto em um vetor numérico (embedding), e depois mede a distância/semelhança entre os vetores.

Embedding = representação vetorial do significado do texto

Cosseno = mede o ângulo entre vetores (sem se importar com magnitude)

Intuição

Dois textos podem ter palavras diferentes, mas significado parecido. Embeddings capturam isso melhor.

Exemplo:

“A capital de Pernambuco é Recife.”

“Recife é a capital pernambucana.”

BLEU pode cair, ROUGE pode cair, mas a similaridade semântica tende a subir.

Intervalo e interpretação

Cosine similarity geralmente vai de -1 a 1, mas em embeddings de linguagem quase sempre fica entre 0 e 1 na prática.

Próximo de 1 = muito semelhante em significado

Próximo de 0 = sem relação

(negativo é raro nesse contexto)

Limitações (vale citar)

Embeddings podem errar nuances (negação, detalhes factuais finos).

Similaridade alta não garante factualidade. (Ex.: duas frases erradas podem ser semanticamente parecidas.)

Ainda é sensível a comprimento e contexto, mas menos que BLEU/ROUGE.

Resposta pronta de entrevista (similaridade)

Similaridade semântica com embeddings mede proximidade de significado, então funciona melhor para avaliação de respostas abertas. Mas não substitui validação factual — por isso usamos em conjunto com outras métricas e, quando necessário, avaliação qualitativa.

5) Como cada parte do seu código funciona (linha por linha, prático)

Vou explicar seu código com foco em “o que eu falaria na entrevista”.

Imports
import os
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

os → ler variáveis de ambiente (config)

sentence_bleu + SmoothingFunction → BLEU com suavização

rouge_scorer → ROUGE-L

SentenceTransformer → embeddings semânticos

cosine_similarity → similaridade vetorial

Carregar modelo de embedding (uma vez só)
EMB_MODEL_NAME = os.getenv("EMB_MODEL_NAME", "all-MiniLM-L6-v2")
_embedder = SentenceTransformer(EMB_MODEL_NAME)

Tenta pegar EMB_MODEL_NAME do ambiente (bom para trocar modelo sem mudar código).

Carrega o modelo uma vez e mantém em memória (cache).
Isso evita recarregar a cada requisição (performance).

Entrevista: “Eu carrego o modelo de embeddings como singleton para reduzir latência.”

Configurar ROUGE e smoothing do BLEU
_rouge = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
_smooth = SmoothingFunction().method1

ROUGE-L configurado.

use_stemmer=True → reduz palavras ao “radical” (ex.: “correndo” ~ “correr”), aumentando robustez.

Smoothing do BLEU para evitar zero em textos curtos.

Função bleu(reference, candidate)
def bleu(reference: str, candidate: str) -> float:
    ref_tokens = reference.split()
    cand_tokens = candidate.split()
    return float(sentence_bleu([ref_tokens], cand_tokens, smoothing_function=_smooth))

O que faz:

Divide a referência em tokens (por espaço).

Divide o candidato em tokens.

Calcula BLEU de frase (sentence_bleu) com smoothing.

Retorna float.

Ponto forte:

simples e rápido

Limitação:

tokenização por .split() é básica (pontuação pode atrapalhar).
Se você quiser evoluir, poderia usar um tokenizer melhor.

Função rouge_l(reference, candidate)
def rouge_l(reference: str, candidate: str) -> float:
    scores = _rouge.score(reference, candidate)
    return float(scores["rougeL"].fmeasure)

O que faz:

Calcula ROUGE (gera precision/recall/f1 internamente).

Retorna o f-measure do ROUGE-L (equilíbrio de precisão e recall).

Por que fmeasure:

é uma forma equilibrada de pontuar (nem só recall nem só precision).

Função semantic_similarity(reference, candidate)
def semantic_similarity(reference: str, candidate: str) -> float:
    e1 = _embedder.encode(reference)
    e2 = _embedder.encode(candidate)
    return float(cosine_similarity([e1], [e2])[0][0])

O que faz:

Gera embedding da referência (e1).

Gera embedding do candidato (e2).

Calcula cosine similarity.

Retorna o valor escalar.

Detalhe:

cosine_similarity espera matriz 2D, por isso [e1] e [e2].

O resultado é uma matriz 1x1 → pega [0][0].

Função calculate_all(reference, candidate)
def calculate_all(reference: str, candidate: str) -> dict:
    return {
        "bleu": round(bleu(reference, candidate), 4),
        "rougeL": round(rouge_l(reference, candidate), 4),
        "similarity": round(semantic_similarity(reference, candidate), 4),
    }

O que faz:

chama as 3 funções

arredonda para 4 casas

retorna um dicionário fácil de renderizar no HTML / API

Entrevista: “Centralizo o cálculo em calculate_all para padronizar saída e simplificar UI e logs.”

6) Resumo curto (cola de entrevista)

Você pode decorar isso:

BLEU

similaridade textual por n-grams

bom para tarefas “exatas” (tradução)

ruim para paráfrases e referência curta

ROUGE-L

sobreposição de conteúdo via maior subsequência comum

bom para resumo e conteúdo

ainda depende de texto literal

Similaridade semântica (cosseno + embeddings)

mede proximidade de significado

bom para respostas abertas

não garante factualidade (precisa curadoria humana/checagem)

E sobre o código:

carrega embeddings uma vez (cache)

usa stemming no ROUGE para ser mais robusto

usa smoothing no BLEU para não zerar em frases curtas

calculate_all padroniza o retorno

7) “Pergunta de entrevistador” e como responder

Pergunta: “Por que suas métricas deram baixo se a resposta estava correta?”
Resposta pronta:

Porque BLEU e ROUGE dependem muito do texto de referência. Se a referência é curta (“Recife”) e o modelo responde com uma frase completa, a correspondência literal cai. Por isso é importante ter boas referências e usar uma métrica semântica para complementar.

Pergunta: “Qual métrica você usaria para curadoria de chatbot?”
Resposta pronta:

Usaria similaridade semântica como base e complementaria com checagens qualitativas/factuais, porque BLEU/ROUGE podem penalizar reescritas corretas.


RESUMO ENTREVISTA 


Perfeito — aqui está um pitch profissional de entrevista que você pode falar com naturalidade para explicar seu módulo de métricas.
Vou te dar 3 versões:

🎤 versão 30 segundos (curta)

🎤 versão 60 segundos (ideal)

🎤 versão técnica aprofundada (se entrevistador for especialista)

🎤 Pitch — versão curta (30s)

Eu implementei um módulo de avaliação automática de respostas de LLM usando três métricas complementares: BLEU, ROUGE-L e similaridade semântica com embeddings. BLEU mede similaridade textual literal, ROUGE mede sobreposição de conteúdo e a similaridade semântica avalia proximidade de significado. Uso as três juntas porque cada uma cobre limitações das outras, criando uma avaliação mais robusta e próxima do comportamento real de sistemas de IA em produção.

🎤 Pitch ideal (60s — use esse)

Nesse projeto eu construí um pipeline de avaliação de respostas de LLM usando três métricas principais. A primeira é BLEU, que mede correspondência textual baseada em n-grams e é útil quando queremos verificar se a resposta segue uma estrutura esperada. A segunda é ROUGE-L, que mede a maior subsequência comum entre textos e avalia sobreposição de conteúdo, sendo comum em tarefas de resumo. A terceira é similaridade semântica, onde uso embeddings para comparar significado em vez de palavras exatas.

Eu uso as três em conjunto porque nenhuma métrica isolada é confiável para avaliação de modelos generativos. BLEU e ROUGE podem penalizar respostas corretas mas reformuladas, enquanto a similaridade semântica captura significado mas não garante factualidade. Então o sistema combina sinais estruturais e semânticos para produzir uma avaliação mais robusta, semelhante a pipelines reais de validação de IA.

🎤 Pitch técnico (para entrevistador senior)

O módulo calcula BLEU com smoothing para evitar penalização excessiva em frases curtas, ROUGE-L com stemming para aumentar robustez lexical e similaridade semântica via embeddings SentenceTransformer e cosine similarity. O modelo de embedding é carregado uma única vez para reduzir latência. Centralizei a lógica em uma função agregadora que retorna scores normalizados, facilitando logging, análise comparativa e integração com UI ou experiment tracking. A escolha de múltiplas métricas segue prática comum em avaliação de LLM, já que métricas baseadas apenas em n-gram não capturam equivalência semântica e métricas semânticas não detectam erros factuais.

🧠 Frases extras que impressionam entrevistador

Use naturalmente se perguntarem mais:

Sobre design

Eu mantive o modelo de embeddings em memória como singleton para evitar overhead de carregamento a cada requisição.

Sobre avaliação de LLM

Métricas automáticas são úteis para triagem, mas avaliação final sempre deve incluir validação qualitativa.

Sobre limitações

Nenhuma métrica automática consegue capturar completamente qualidade de linguagem natural, por isso a abordagem mais robusta é combinar métricas.

🎯 Versão ultra-curta (caso te interrompam)

Eu combinei métricas lexicais e semânticas para avaliar respostas de LLM, porque cada tipo mede um aspecto diferente da qualidade.

✅ Dica final de entrevista:
Fale devagar e com segurança. O conteúdo já é avançado — não precisa parecer complicado.

✅ Se quiser, posso também te preparar um mini-simulado de entrevista técnica com perguntas reais que recrutadores fazem sobre avaliação de LLM.