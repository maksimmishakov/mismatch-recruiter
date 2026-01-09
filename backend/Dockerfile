FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN find /app -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

EXPOSE 80

# Исправлено: wsgi:app вместо main:app
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "4", "--timeout", "120", "wsgi:app"]
