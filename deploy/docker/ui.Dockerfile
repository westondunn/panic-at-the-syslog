# UI service - Next.js web dashboard
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY services/ui/package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY services/ui/ ./

# Ensure public dir exists (Next.js expects it)
RUN mkdir -p public

# Build the Next.js app
RUN npm run build

# Production image
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Copy built app and dependencies
COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001 && \
    chown -R nextjs:nodejs /app

USER nextjs

EXPOSE 3000

CMD ["npx", "next", "start"]
