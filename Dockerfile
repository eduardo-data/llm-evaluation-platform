FROM python:3.11-slim

WORKDIR /app

# Dependências mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

COPY app /app

EXPOSE 5000

CMD ["python", "main.py"]