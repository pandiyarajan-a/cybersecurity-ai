FROM docker.n8n.io/n8nio/n8n

USER root

# Install Docker CLI using Alpine's package manager
RUN apk update && apk add docker-cli \
 && addgroup -S docker \
 && adduser node docker \
 && rm -rf /var/lib/apt/lists/*

USER node

