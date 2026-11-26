FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# NLTK tokenizers and stopwords for sumy, the extractive pre-pass
# (nltk>=3.9 reads punkt_tab).
RUN python -c "import nltk; [nltk.download(p, quiet=True) for p in ('punkt', 'punkt_tab', 'stopwords')]"

COPY api ./api
COPY nlp ./nlp

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/readyz', timeout=4).status == 200 else 1)"

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
