FROM python:3.12-slim

# Установите зависимости ОС
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установите рабочую директорию
WORKDIR /app

# Скопируйте requirements
COPY requirements.txt .

# Установите Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте весь код
COPY . .

# Экспортируйте порт
EXPOSE 5000

# Создайте папки для логов и uploads
RUN mkdir -p logs uploads

ENV FLASK_ENV=production
ENV FLASK_DEBUG=False
ENV FLASK_HOST=0.0.0.0
ENV FLASK_PORT=5000

# Команда для запуска
CMD ["python", "run.py"]
