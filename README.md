# Incident & RCA Platform

A backend that ingests production alerts, deduplicates them into incidents, tracks each incident's lifecycle and timeline, reports reliability metrics (MTTA/MTTR) with SQL, and drafts RCAs with an LLM for a human to review.

Built around a problem I know from on-call work: alert noise, incident tracking, and writing RCAs after the fact.

## Status

**v0.1 (done):** FastAPI app skeleton, health check, async SQLAlchemy + asyncpg, Alembic (async), PostgreSQL in Docker Compose, pytest with httpx. Verified from a fresh clone.

## Release plan

- **v0.2: Incidents core.** Services, incidents, state machine with optimistic locking, timeline events
- **v0.3: MVP.** Alert ingestion with database-level deduplication and idempotency keys, SQL analytics (MTTR, noisy services), AI-drafted RCAs with human approval
- **v0.4: AI done responsibly.** Eval set, guardrails (redaction, input limits, failure handling), cost/latency logging, Markdown RCA + runbook export, end-to-end test

## Tech stack

Python 3.12 · FastAPI · Pydantic v2 · SQLAlchemy 2.0 (async) + asyncpg · Alembic · PostgreSQL 16 · pytest + pytest-asyncio + testcontainers · httpx · uv · Docker Compose · ruff · pre-commit

## Run locally

Requirements: [uv](https://docs.astral.sh/uv/), Docker Desktop.

```bash
cp .env.example .env
uv sync
docker compose up -d          # wait for "healthy": docker compose ps
uv run alembic upgrade head
uv run pytest
uv run uvicorn app.main:app --reload
```
Then open http://localhost:8000/docs.

## Out of scope (on purpose)

Kubernetes, Terraform, AWS, a UI, microservices, auth provider integration, autonomous agents, and multi-tenancy. The goal is depth in API design, PostgreSQL and data correctness rather than breadth of infrastructure. Possible future work: a transactional outbox with a worker (Redis Streams or Kafka), retries and a dead-letter queue, and Prometheus/Grafana metrics.