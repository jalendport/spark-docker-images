FROM redis:7.2-alpine

# A development default; override REDIS_PASSWORD at run time for anything real
# hadolint ignore=DL3064
ENV REDIS_PASSWORD=root

CMD ["sh", "-c", "exec redis-server --requirepass \"$REDIS_PASSWORD\""]
