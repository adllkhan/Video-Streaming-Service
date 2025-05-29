FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app/src

WORKDIR /app

# RUN pip install uv --no-cache

COPY pyproject.toml .

# RUN uv pip install . \
#     --system \
#     --no-cache

RUN pip install --no-cache-dir .

COPY . .

EXPOSE 8000

CMD ["python", "src/main.py"]
