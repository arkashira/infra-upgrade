# TECH_SPEC.md

## 1. Overview

**infra‑upgrade** is a Python‑based automation framework that orchestrates AI infrastructure upgrades while minimizing downtime and maximizing throughput.  
The system is composed of a **controller** that schedules upgrade jobs, a **compatibility checker** that validates target environments, a **performance optimizer** that tunes resource allocation, and an **error‑minimizer** that monitors and rolls back failures. The design follows a modular, event‑driven architecture that allows each component to be independently scaled and replaced.

---

## 2. Architecture

```
┌─────────────────────┐
│  Upgrade Orchestrator │  ←  REST/GRPC API
└───────┬──────────────┘
        │
        │ 1. Schedule upgrade
        ▼
┌─────────────────────┐
│  Compatibility Engine│  ←  Checks target stack
└───────┬──────────────┘
        │
        │ 2. Validate
        ▼
┌─────────────────────┐
│  Performance Optimizer│  ←  Resource tuning
└───────┬──────────────┘
        │
        │ 3. Apply
        ▼
┌─────────────────────┐
│  Error‑Minimizer      │  ←  Monitoring & rollback
└───────┬──────────────┘
        │
        │ 4. Finalize
        ▼
┌─────────────────────┐
│  Reporting & Metrics │  ←  Prometheus / Grafana
└─────────────────────┘
```

* **Event Bus** – All components communicate via a lightweight message queue (Redis Streams).  
* **State Store** – PostgreSQL (or SQLite for dev) holds job metadata, rollback points, and audit logs.  
* **Container Orchestration** – Docker + Docker‑Compose for local dev; Kubernetes for production.

---

## 3. Core Components

| Component | Responsibility | Key Modules |
|-----------|----------------|-------------|
| **Orchestrator** | Job lifecycle, API gateway | `src/orchestrator/api.py`, `src/orchestrator/worker.py` |
| **Compatibility Engine** | Detects version conflicts, missing dependencies | `src/compatibility/checker.py` |
| **Performance Optimizer** | Auto‑scales GPU/CPU, configures batch sizes | `src/optimizer/optimizer.py` |
| **Error‑Minimizer** | Monitors logs, triggers rollback | `src/error_handler/handler.py` |
| **Reporting** | Aggregates metrics, exposes Prometheus endpoints | `src/reporting/metrics.py` |

---

## 4. Data Model

| Table | Columns | Description |
|-------|---------|-------------|
| `upgrade_jobs` | `id`, `status`, `created_at`, `started_at`, `completed_at`, `target_version`, `source_version`, `config_hash` | Stores job metadata |
| `rollback_points` | `job_id`, `snapshot_id`, `timestamp` | Points to pre‑upgrade state |
| `compatibility_report` | `job_id`, `component`, `current`, `required`, `status` | Results of compatibility checks |
| `performance_metrics` | `job_id`, `metric_name`, `value`, `timestamp` | Runtime performance data |

All tables are versioned via Alembic migrations.

---

## 5. Key APIs / Interfaces

### 5.1 REST API (FastAPI)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/jobs` | POST | Submit a new upgrade job. Body: `{ "target_version": "v2.1", "config": {...} }` |
| `/jobs/{id}` | GET | Retrieve job status and logs. |
| `/jobs/{id}/cancel` | POST | Cancel a running job. |
| `/metrics` | GET | Prometheus scrape endpoint. |

### 5.2 Internal Message Formats

```json
{
  "type": "upgrade_start",
  "job_id": "uuid",
  "payload": {
    "target_version": "v2.1",
    "config_hash": "abcd1234"
  }
}
```

All messages are JSON‑encoded and routed through Redis Streams.

---

## 6. Technology Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **Language** | Python 3.12 | Mature ecosystem, async support |
| **Web Framework** | FastAPI | Fast, async, OpenAPI docs |
| **Message Queue** | Redis Streams | Low‑latency, persistence |
| **Database** | PostgreSQL (dev: SQLite) | ACID, JSONB support |
| **Containerization** | Docker | Reproducible builds |
| **Orchestration** | Kubernetes (prod), Docker‑Compose (dev) | Scalability |
| **Monitoring** | Prometheus + Grafana | Metrics collection |
| **CI/CD** | GitHub Actions | Build, test, lint, publish |
| **Testing** | pytest, httpx | Unit & integration tests |
| **Linting** | ruff, mypy | Code quality |
| **Documentation** | MkDocs + MkDocs‑Material | Project docs |

---

## 7. Dependencies

| Category | Package | Version |
|----------|---------|---------|
| **Core** | fastapi | ^0.115.0 |
| | uvicorn | ^0.30.6 |
| | redis | ^5.1.0 |
| | sqlalchemy | ^2.0.32 |
| | alembic | ^1.13.3 |
| | pydantic | ^2.9.2 |
| **Testing** | pytest | ^8.3.3 |
| | httpx | ^0.27.2 |
| | pytest-asyncio | ^0.23.8 |
| **Monitoring** | prometheus‑client | ^0.21.0 |
| **Linting** | ruff | ^0.6.8 |
| | mypy | ^1.13.0 |
| **Deployment** | docker | n/a |
| | kubernetes | n/a |

All dependencies are pinned in `pyproject.toml`. Optional extras:

```toml
[tool.poetry.extras]
dev = ["pytest", "ruff", "mypy"]
```

---

## 8. Deployment

### 8.1 Local Development

```bash
# Install dependencies
poetry install --with dev

# Run Redis
docker run -d --name redis -p 6379:6379 redis:7

# Run database
docker run -d --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:16

# Apply migrations
poetry run alembic upgrade head

# Start API
poetry run uvicorn src.orchestrator.api:app --reload
```

### 8.2 Production (Kubernetes)

1. **Build image**

```bash
docker build -t axentx/infra-upgrade:latest .
docker push axentx/infra-upgrade:latest
```

2. **Deploy**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: infra-upgrade
spec:
  replicas: 3
  selector:
    matchLabels:
      app: infra-upgrade
  template:
    metadata:
      labels:
        app: infra-upgrade
    spec:
      containers:
      - name: infra-upgrade
        image: axentx/infra-upgrade:latest
        envFrom:
        - secretRef:
            name: infra-upgrade-secrets
        ports:
        - containerPort: 8000
```

3. **Service**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: infra-upgrade
spec:
  selector:
    app: infra-upgrade
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
```

4. **Ingress** – expose via Ingress Controller with TLS.

5. **Monitoring** – Deploy Prometheus scrape config and Grafana dashboards.

---

## 9. Security & Compliance

* **Secrets** – Stored in Kubernetes Secrets or Vault.  
* **Authentication** – API uses JWT Bearer tokens (FastAPI‑JWT).  
* **Audit** – All job actions are logged to `upgrade_jobs` table and forwarded to ELK stack.  
* **Rate Limiting** – Implemented via FastAPI middleware (slowapi).  

---

## 10. Testing Strategy

| Test Type | Tool | Coverage |
|-----------|------|----------|
| Unit | pytest | 90%+ |
| Integration | pytest + httpx | 80%+ |
| End‑to‑End | Docker Compose | 70%+ |
| Performance | Locust | 95%+ |

Test suites are run on every PR via GitHub Actions.

---

## 11. Roadmap (Next 3 Months)

1. **Finalize Tech Stack** – Lock on PostgreSQL, Redis, and Docker/K8s.  
2. **Implement Compatibility Engine** – Add support for vLLM, SGLang.  
3. **Performance Optimizer** – Auto‑scale GPU memory based on workload.  
4. **Error‑Minimizer** – Add circuit breaker and automated rollback.  
5. **CI/CD Pipeline** – Automate image build, push, and Helm chart deployment.  

---

## 12. Appendix

### 12.1 Directory Layout

```
infra-upgrade/
├── business/          # Business rules
├── src/
│   ├── orchestrator/  # API & worker
│   ├── compatibility/
│   ├── optimizer/
│   ├── error_handler/
│   └── reporting/
├── tests/
├── alembic/           # DB migrations
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── README.md
└── TECH_SPEC.md
```

### 12.2 Contact

- **Lead Engineer** – [email@example.com](mailto:email@example.com)  
- **Slack** – `#infra-upgrade`

---
