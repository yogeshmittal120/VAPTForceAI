# VAPTForceAI

**Autonomous Security Assessment & Remediation**

VAPTForceAI is an AI-assisted security assessment platform. The MVP starts with repository-based security assessments and is designed to grow into a multi-agent workflow for finding, analyzing, and safely remediating vulnerabilities.

## Phase 1 scope

- FastAPI backend with versioned REST endpoints
- SQLite persistence through SQLAlchemy 2.x
- Assessment creation, listing, and retrieval
- Scan type selection: SAST, dependency scanning, and secret scanning
- Provider-independent LLM interface and registry (no provider credentials required yet)
- Automated tests for API and provider-registry foundations

> Scanners and LLM provider adapters are integration work for later phases. Creating an assessment in Phase 1 does not execute a security scan.

## Technology

- Python 3.11+
- FastAPI and Uvicorn
- SQLAlchemy 2.x
- SQLite
- Pydantic Settings
- Pytest and HTTPX

## Project structure

```text
VAPTForceAI/
├── app/
│   ├── api/routes/       # HTTP endpoints
│   ├── core/             # Settings and shared configuration
│   ├── db/               # SQLAlchemy base and sessions
│   ├── llm/              # Provider-independent LLM contract and registry
│   ├── models/           # Database models
│   ├── schemas/          # Pydantic API schemas
│   ├── services/         # Business logic
│   └── main.py           # FastAPI application
├── tests/
├── .env.example
├── requirements.txt
└── requirements-dev.txt
```

## Local setup

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

### 3. Configure environment

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

The defaults use a local SQLite database and disable LLM calls. No API keys are needed for Phase 1.

### 4. Run the API

```bash
uvicorn app.main:app --reload
```

- API root: http://127.0.0.1:8000/
- Swagger UI: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/api/v1/health

The SQLite database file is created as `vaptforceai.db` in the working directory when the application starts.

## Initial API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/v1/health` | Check API health |
| POST | `/api/v1/assessments` | Create an assessment |
| GET | `/api/v1/assessments` | List assessments |
| GET | `/api/v1/assessments/{assessment_id}` | Retrieve one assessment |

### Create an assessment

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/assessments" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sample Python API",
    "repository_url": "https://github.com/example/sample-api",
    "scan_types": ["sast", "dependency", "secret"]
  }'
```

Assessment creation stores the request with status `created`. It does not clone the repository or run scanners yet.

## Run tests

```bash
pytest -q
```

## Configuration

Settings are loaded from environment variables and optionally from `.env`.

| Variable | Default | Description |
|---|---|---|
| `APP_NAME` | `VAPTForceAI` | Application name |
| `ENVIRONMENT` | `development` | Runtime environment |
| `API_V1_PREFIX` | `/api/v1` | Versioned API prefix |
| `DATABASE_URL` | `sqlite:///./vaptforceai.db` | SQLAlchemy database URL |
| `LLM_PROVIDER` | `none` | Provider registry key; adapters will be added later |

## Security and safety principles

- Repository scanning and active testing must only run against targets the user is authorized to assess.
- Remediation is proposal-first. A human must approve a patch before it is applied.
- Future active testing will use explicit target allowlists, bounded execution, and non-destructive defaults.
- Never commit `.env`, API keys, tokens, or scan credentials.

## Roadmap

1. **Phase 1 – Foundation:** API, SQLite, assessment records, configuration, tests, LLM abstraction.
2. **Phase 2 – Scanning engine:** repository intake, SAST, dependency and secret scanners, normalized findings.
3. **Phase 3 – Agentic analysis:** LangGraph orchestration, finding correlation, prioritization, LLM-backed analysis.
4. **Phase 4 – Remediation:** patch proposals, human approval, isolated working branches.
5. **Phase 5 – Validation:** tests, rescans, before/after verification.
6. **Phase 6 – Reporting and extended VAPT:** reports, dashboard APIs, authorized DAST capabilities.
