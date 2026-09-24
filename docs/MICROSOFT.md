# Microsoft-oriented architecture

The backend includes optional adapters for Microsoft Foundry and Azure OpenAI, with secrets kept server-side.

Conceptual flow:

```text
Frontend UI
   ↓
FastAPI API
   ↓
Intent Router
   ↓
Specialist / Safety Workflow
   ↓
Model Router
   ├── Demo Engine
   ├── Microsoft Foundry
   └── Azure OpenAI
   ↓
Audit + persistence
   ├── PostgreSQL + pgvector
   └── Redis
```

The UI also contains Microsoft-ecosystem oriented sections for knowledge, identity, monitoring, security, partner/program workflows and business intelligence. Any live external metrics or incidents should be sourced from authoritative APIs before being represented as production data.
