# Stage 1: Build React application
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY frontend/ .

# Build production bundle
RUN npm run build

# Stage 2: Serve with Node
FROM node:18-alpine

WORKDIR /app

# Install serve to serve static files
RUN npm install -g serve

# Copy build from previous stage
COPY --from=builder /app/build ./build

EXPOSE 3000

# Serve production build
CMD ["serve", "-s", "build", "-l", "3000"]