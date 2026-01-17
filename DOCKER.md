# AvantDeSigner - Docker Deployment Guide

## Quick Start

### Prerequisites
- Docker Desktop installed
- 8GB RAM minimum
- 10GB disk space

### Start Application
```bash
docker-compose up -d
```

### Access
- Frontend: http://localhost:3000
- API: http://localhost:8000
- Health: http://localhost:8000/health

### Stop Application
```bash
docker-compose down
```

---

## Development

### Build Services
```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build ai-service
docker-compose build web
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f ai-service
docker-compose logs -f web
```

### Restart Services
```bash
# Restart all
docker-compose restart

# Restart specific
docker-compose restart ai-service
```

---

## Volumes

### Persistent Data
- `ai-cache`: Hugging Face models cache
- `rag-cache`: FAISS index and embeddings

### Clear Cache
```bash
docker-compose down -v  # WARNING: Deletes all volumes
```

---

## Troubleshooting

### Service Won't Start
```bash
# Check logs
docker-compose logs ai-service

# Rebuild
docker-compose build --no-cache ai-service
docker-compose up -d
```

### Port Already in Use
```bash
# Change ports in docker-compose.yml
ports:
  - "3001:3000"  # Frontend
  - "8001:8000"  # API
```

### Out of Memory
```bash
# Increase Docker memory limit in Docker Desktop settings
# Minimum: 8GB recommended
```

---

## Production Deployment

### Environment Variables
Create `.env` file:
```env
NODE_ENV=production
AI_SERVICE_URL=http://ai-service:8000
PYTHONUNBUFFERED=1
```

### Security
- Use reverse proxy (nginx)
- Enable HTTPS
- Set up firewall rules
- Use secrets management

### Monitoring
```bash
# Resource usage
docker stats

# Health checks
curl http://localhost:8000/health
```

---

## Architecture

```
┌─────────────────┐
│   Next.js Web   │ :3000
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Python AI API  │ :8000
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  HF Models      │ (cached)
│  FAISS Index    │ (cached)
└─────────────────┘
```

---

## Updates

### Pull Latest Changes
```bash
git pull
docker-compose build
docker-compose up -d
```

### Update Dependencies
```bash
# Python
cd python-ai
pip freeze > requirements.txt

# Node.js
npm update

# Rebuild
docker-compose build
```
