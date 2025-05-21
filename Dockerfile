FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client

COPY pyproject.toml .

RUN pip install --no-cache-dir .

COPY . .

EXPOSE 8000

CMD ["python", "src/main.py"]