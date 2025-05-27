FROM python:3.13-slim

WORKDIR /app

RUN pip install uv --no-cache

COPY pyproject.toml .

RUN uv pip install . \
    --system \
    --no-cache

COPY . .

EXPOSE 8000

CMD ["uv", "run", "src/main.py"]
