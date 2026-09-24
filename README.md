# Rural Guardian Intelligence Platform

**Microsoft Agent-a-Thon prototype**  
**One AI platform for safer, smarter rural communities.**

Rural Guardian Intelligence Platform is a multi-agent platform concept for rural communities. The current submission packages the finalized frontend UI together with a FastAPI backend, PostgreSQL + pgvector foundation, Redis rate limiting, safety-aware routing, audit logging, and optional Microsoft Foundry / Azure OpenAI model adapters.

## What is included

- Finalized Rural Guardian Intelligence Platform frontend UI with the current sections and visual design.
- Command Center, Agent Hub, AI Copilot, Alerts & Safety, Knowledge & RAG, Analytics & Impact.
- Microsoft Ecosystem, Business Intelligence, Problem Center, Certification Hub, Voucher Protection, Profile and Governance sections.
- Interactive UI elements already present in the frontend, including navigation, cards, panels, map views and Copilot controls.
- FastAPI backend with authentication/session handling, CSRF protection, rate limiting, agent routing, safety policy and audit logging.
- PostgreSQL + pgvector and Redis services.
- Optional OpenRouter, Microsoft Foundry, and Azure OpenAI model adapters.
- Demo mode so the project can be run without live model credentials.

## Quick run (recommended)

1. Copy `.env.example` to `.env`.
2. Keep `MODEL_PROVIDER=demo` for the safe no-credentials demo.
3. Run:

```bash
docker compose up --build
```

4. Open **http://localhost:5173**.
5. Backend health endpoint: **http://localhost:8000/api/health**.

Demo login:
- Email: `admin@example.com`
- Password: `ChangeMe!123`


## OpenRouter

The backend can use OpenRouter through its OpenAI-compatible API. OpenRouter documents the base URL as `https://openrouter.ai/api/v1`; keep the key on the server in `.env`, never in the frontend. citeturn675147search1turn675147search5

```env
MODEL_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-...
OPENROUTER_MODEL=openai/gpt-4o-mini
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

Optional provider fallbacks can be supplied as a comma-separated list; OpenRouter supports model fallbacks in the request body. citeturn675147search4

## Microsoft Foundry

To connect a deployed Foundry agent later, set:

```env
MODEL_PROVIDER=foundry
FOUNDRY_PROJECT_ENDPOINT=https://<resource>.services.ai.azure.com/api/projects/<project>
FOUNDRY_AGENT_NAME=<agent-name>
```

The backend keeps credentials server-side. Do not put secrets in the frontend.

## Azure OpenAI fallback

```env
MODEL_PROVIDER=azure_openai
AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com
AZURE_OPENAI_API_KEY=<secret>
AZURE_OPENAI_DEPLOYMENT=<deployment-name>
```

## Backend tests

```bash
cd backend
pytest -q
```

Expected local result for the included tests: **4 passed**.

## Important demo note

The current frontend is intentionally preserved as the finalized UI and does not need live backend calls to render the submitted experience. The backend is packaged alongside it and provides the authenticated API, routing and model integration foundation for the next iteration.

Demo/placeholder values in the UI are not presented as live production measurements.

## Project structure

```text
Rural-Guardian-Intelligence-Platform/
├── frontend/
│   ├── index.html
│   ├── Dockerfile
│   └── nginx.conf
├── backend/
│   ├── app/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── docs/
├── scripts/
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

**Made by Sunny**

## Functional AI Copilot

The AI Copilot is connected to the backend API. In development mode the UI can use the seeded demo account automatically. For real AI responses, set `MODEL_PROVIDER=openrouter` and add your OpenRouter key in `.env`. The key stays server-side.

## Verification performed on the packaged source

- Python source compilation passed.
- Backend test suite passed: 4 tests.
- Frontend JavaScript syntax check passed.
- ZIP integrity check passed.

Docker execution cannot be performed in this build environment when the Docker daemon/CLI is unavailable. On a machine with Docker Desktop, use `docker compose up --build` and verify `/api/health` and `/api/readiness` before submission.
