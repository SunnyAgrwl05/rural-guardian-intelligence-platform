# 🌾 Rural Guardian Intelligence Platform

> **One AI. Multiple Agents. Safer Rural Communities.**

**Rural Guardian Intelligence Platform** is a multi-agent AI platform concept built for rural communities. It combines a unified **AI Copilot**, domain-specific specialist agents, safety-aware routing, knowledge/RAG foundations, governance, audit logging, and a production-oriented backend architecture.

Built as a **Microsoft Agent-a-Thon prototype**.

---

## 🚀 Why Rural Guardian?

Rural communities face problems that span multiple domains—agriculture, disaster safety, health, education, rural business, and digital compliance.

A generic chatbot treats every request the same.

**Rural Guardian takes a different approach:**

**User → AI Copilot → Intent & Risk Routing → Specialist Agent → Safety Guard → Actionable Response**

This makes the platform modular, domain-aware, and designed with responsible AI and operational safety in mind.

---

## ✨ Platform Highlights

| Capability | What it does |
|---|---|
| 🤖 **AI Copilot** | Natural-language entry point for rural community requests |
| 🧭 **Intent Router** | Identifies domain and risk context before routing |
| 🌾 **Agriculture Agent** | Supports agriculture and crop-related scenarios |
| 🌧️ **Disaster Agent** | Handles emergency and environmental safety scenarios |
| 🩺 **Health Safety Agent** | Provides safety-focused health guidance |
| 🎓 **Education Agent** | Supports learning and education workflows |
| 🏪 **Rural Business Agent** | Supports rural business and opportunity workflows |
| 🛡️ **Voucher & License Abuse Monitor** | Detects suspicious misuse without generating or validating codes |
| 📚 **Knowledge & RAG** | Foundation for grounded responses |
| 🚨 **Alerts & Safety** | Risk-aware safety workflows |
| 📊 **Analytics & Impact** | Operational and community insights |
| 🔐 **Governance & Audit** | Authentication, logging, safety controls and traceability |

---

## 🧠 AI Copilot

The Copilot is the central interaction layer.

A user can describe a problem in natural language instead of knowing which agent to use.

### Example

> **“My village has heavy rain and wheat is ready for harvest. What should I do?”**

The platform identifies the situation as a potential disaster context and routes it to the **Disaster Agent**, which provides immediate safety-focused guidance and directs users to official local authorities for live alerts.

### Agentic flow

```text
┌───────────────┐
│     User      │
└───────┬───────┘
        ↓
┌───────────────┐
│  AI Copilot   │
└───────┬───────┘
        ↓
┌────────────────────┐
│ Intent + Risk      │
│ Router             │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ Specialist Agent   │
│ Agriculture        │
│ Disaster           │
│ Health             │
│ Education          │
│ Business           │
│ Compliance         │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ Safety / Compliance│
│ Guard              │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ Final Response     │
└────────────────────┘
```

---

## 🏗️ Architecture

The backend is designed around a modular API and agent-routing foundation:

```text
Frontend
   │
   ▼
FastAPI API
   │
   ├── Authentication / Sessions
   ├── CSRF Protection
   ├── Rate Limiting
   ├── Intent & Agent Routing
   ├── Safety Policy
   ├── Audit Logging
   │
   ├───────────────┬─────────────────┐
   ▼               ▼                 ▼
PostgreSQL       Redis        AI Provider Adapters
+ pgvector                         │
                         ┌─────────┼─────────┐
                         ▼         ▼         ▼
                     OpenRouter Foundry  Azure OpenAI
```

### Engineering foundations

- **FastAPI** API layer
- **SQLAlchemy 2** data layer
- **PostgreSQL + pgvector** for persistent and vector-oriented knowledge foundations
- **Redis** for rate limiting
- **Alembic** for database migrations
- **JWT/session authentication**
- **Argon2** password hashing
- **CSRF protection**
- **Request IDs and structured logging**
- **Health/readiness/metrics endpoints**
- **Docker Compose + Nginx**
- Server-side model credentials; no secrets in the frontend

---

## 🛡️ Responsible AI & Safety

Safety is a shared layer across the platform rather than a feature of one agent.

The system is designed to:

- Detect potential misuse, fraud, policy violations, and operational risk
- Avoid generating, validating, storing, or distributing secrets, keys, vouchers, license codes, or premium benefits
- Recommend verification, user education, internal review, logging, and escalation when risk is detected
- Direct high-risk emergency scenarios toward official authorities
- Keep model credentials server-side
- Support auditable decisions through logging and request tracking

> **Risk detection is not accusation.** The platform is designed to identify signals and recommend safe next steps.

---

## 🧩 Platform Modules

The current frontend experience includes:

- Overview
- Command Center
- Agent Hub
- AI Copilot
- Alerts & Safety
- Knowledge & RAG
- Analytics & Impact
- Specialized Agents
- Microsoft Ecosystem
- Microsoft Business Intelligence
- Microsoft Risk & Reliability
- Certification Hub
- Voucher Protection
- Profile Dashboard
- Admin & Governance
- Settings

---

## ☁️ AI Provider Integrations

The backend includes adapters for:

### OpenRouter

```env
MODEL_PROVIDER=openrouter
OPENROUTER_API_KEY=your-server-side-key
OPENROUTER_MODEL=openai/gpt-4o-mini
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

### Microsoft Foundry

```env
MODEL_PROVIDER=foundry
FOUNDRY_PROJECT_ENDPOINT=https://<resource>.services.ai.azure.com/api/projects/<project>
FOUNDRY_AGENT_NAME=<agent-name>
```

### Azure OpenAI

```env
MODEL_PROVIDER=azure_openai
AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com
AZURE_OPENAI_API_KEY=<server-side-secret>
AZURE_OPENAI_DEPLOYMENT=<deployment-name>
```

**Never commit real credentials.** Use `.env`, which is excluded through `.gitignore`.

---

## 🧪 Demo Mode & Verification

The project includes a demo mode so the frontend and backend foundation can be explored without live model credentials.

### Local verification

```bash
docker compose up --build
```

Then open:

- Frontend: `http://localhost:5173`
- Backend health: `http://localhost:8000/api/health`

Backend tests:

```bash
cd backend
pytest -q
```

The packaged source was verified with:

- Python source compilation
- Backend test suite
- Frontend JavaScript syntax check
- ZIP integrity check

---

## 📁 Project Structure

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

---

## 🌐 Project Links

**Live Frontend:**  
https://rural-guardian-intelligence-platform-1d8ic8odv.vercel.app

**Source Code:**  
https://github.com/SunnyAgrwl05/rural-guardian-intelligence-platform

---

## 🎯 Vision

Rural Guardian is designed around a simple principle:

> **One AI. Multiple Agents. Safer Rural Communities.**

The goal is to turn reusable expertise into specialized, governable AI agents that can support different rural scenarios while sharing a common safety and compliance foundation.

---

## 👨‍💻 Built by Sunny Kumar

**Rural Guardian Intelligence Platform**  
Microsoft Agent-a-Thon Prototype

