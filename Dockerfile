# Multi-stage build for MisMatch Recruiter

# Stage 1: Frontend build
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci --only=production
COPY frontend . 
RUN npm run build

# Stage 2: Backend preparation
FROM python:3.10-slim AS backend-builder
WORKDIR /app/backend
COPY backend/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 3: Final runtime image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=5000 \
    NODE_ENV=production

WORKDIR /app

# Install Node.js for static file serving
RUN apt-get update && apt-get install -y --no-cache \
    nodejs npm \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=backend-builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy backend application
COPY backend ./backend

# Copy frontend build output
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Start application
EXPOSE ${PORT}
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
