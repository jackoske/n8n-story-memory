FROM python:3.11-slim

WORKDIR /app

COPY simple_requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY .env* ./

EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]