FROM node:22-alpine

RUN mkdir -p /app /app-tmp

WORKDIR /app

COPY --chmod=+x ./npm_install.sh /app-tmp/npm_install.sh

# Runs "npm install" if package.json exists but package-lock.json or node_modules do not exist
ENTRYPOINT ["/app-tmp/npm_install.sh"]

CMD ["npm", "run", "dev"]
