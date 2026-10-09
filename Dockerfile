# escada: imagem base por tag (3.13-slim), sem digest; fixar @sha256 quando houver docker na maquina de build
FROM python:3.13-slim

RUN groupadd -g 1000 app && useradd -u 1000 -g 1000 -m -s /bin/bash app

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=app:app . .

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=5)" || exit 1

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "app:app"]
