# Build stage
FROM node:24-alpine as builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Runtime stage
FROM node:24-alpine

WORKDIR /app

# Install serve to run production build
RUN npm install -g serve

COPY --from=builder /app/dist ./dist

# Create non-root user
RUN addgroup -g 1000 appuser && adduser -D -u 1000 -G appuser appuser
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:5173/ || exit 1

EXPOSE 5173

CMD ["serve", "-s", "dist", "-l", "5173"]
