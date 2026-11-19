#!/usr/bin/env bash
# Startet Qdrant und Ollama neben einem laufenden n8n-Container namens "n8n".
set -euo pipefail

docker network create paper-radar 2>/dev/null || echo "Netzwerk paper-radar existiert bereits"
docker network connect paper-radar n8n 2>/dev/null || echo "n8n ist bereits im Netzwerk"

docker run -d --name qdrant --network paper-radar --restart unless-stopped \
  -p 6333:6333 -v qdrant_data:/qdrant/storage qdrant/qdrant

docker run -d --name ollama --network paper-radar --restart unless-stopped \
  -v ollama_data:/root/.ollama ollama/ollama

docker exec ollama ollama pull nomic-embed-text

echo "Prüfen:"
docker exec n8n wget -qO- http://qdrant:6333 && echo
docker exec n8n wget -qO- http://ollama:11434 && echo
