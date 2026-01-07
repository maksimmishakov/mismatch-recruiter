# Build stage
FROM node:20-alpine as builder

WORKDIR /app

COPY package.json package-lock.json .

RUN npm ci --only=production && cp -R node_modules /prod_node_modules && npm ci

COPY . .

RUN npm run build

# Production stage
FROM node:20-alpine

WORKDIR /app

RUN npm install -g serve

COPY --from=builder /app/dist ./dist
COPY --from=builder /prod_node_modules ./node_modules

USER node

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:3000 || exit 1

EXPOSE 3000

CMD ["serve", "-s", "dist", "-l", "3000"]
