FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# For development: use Flask dev server
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
