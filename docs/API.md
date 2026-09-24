# Rural Guardian Intelligence Platform — API

## Core endpoints

- `GET /api/health` — liveness
- `GET /api/readiness` — PostgreSQL + Redis readiness
- `GET /api/metrics` — lightweight service metrics
- `GET /api/modules` — registered agent modules
- `GET /api/auth/csrf` — CSRF token
- `POST /api/auth/login` — session login
- `POST /api/auth/demo-login` — development-only seeded login
- `GET /api/auth/me` — current user
- `POST /api/auth/logout` — session logout
- `POST /api/chat` — authenticated multi-agent chat
- `GET /api/admin/audit` — admin audit log

## OpenRouter

Put the key only in the backend `.env` file:

```env
MODEL_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-...
OPENROUTER_MODEL=openai/gpt-4o-mini
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

The frontend never receives the API key.

## Chat request

```json
{
  "session_id": 1,
  "module": "rural-guardian",
  "message": "My crop is affected by heavy rain. What should I check?"
}
```

The backend performs routing, safety-aware prompting, model invocation, persistence and audit logging.
