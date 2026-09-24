# Rural Guardian Intelligence Platform — Run Guide

## 1. Start

```bash
cp .env.example .env
docker compose up --build
```

Open:
- Frontend: http://localhost:5173
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Health: http://localhost:8000/api/health
- Readiness: http://localhost:8000/api/readiness

## 2. Demo mode

`.env.example` defaults to:

```env
MODEL_PROVIDER=demo
DEV_SEED=true
```

The frontend can use the development-only demo login automatically. No AI API key is required for the UI/backend smoke demo.

## 3. OpenRouter mode

Edit `.env`:

```env
MODEL_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-your-key
OPENROUTER_MODEL=openai/gpt-4o-mini
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

Restart:

```bash
docker compose down
docker compose up --build
```

Never commit `.env` or an API key to GitHub.

## 4. Backend tests

```bash
cd backend
PYTHONPATH=. pytest -q
```

## 5. Stop

```bash
docker compose down
```

For a clean local database reset only:

```bash
docker compose down -v
```
