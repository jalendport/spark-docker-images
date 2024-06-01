FROM redis:7.2-alpine

ENV REDIS_PASSWORD root

CMD ["sh", "-c", "exec redis-server --requirepass \"$REDIS_PASSWORD\""]
