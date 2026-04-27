FROM python:3.10-slim

WORKDIR /app

# Installation des dépendances système pour PostgreSQL
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# On copie uniquement ce qui est nécessaire pour l'orchestrateur
COPY infra_manager.py .
COPY config.yaml .

CMD ["python", "infra_manager.py"]
