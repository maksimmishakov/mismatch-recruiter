# Stage 1: Build
FROM node:24-alpine as builder

WORKDIR /app

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ .
RUN npm run build

# Stage 2: Runtime
FROM node:24-alpine

WORKDIR /app

RUN npm install -g serve

COPY --from=builder /app/build ./build
COPY --from=builder /app/package*.json ./

EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]
