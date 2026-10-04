# Architecture decisions

ADR = Architecture Decision Record: one entry per significant technical decision, recording what we chose and why.

---

## ADR-001: PostgreSQL over MongoDB
Date: 2026-10-04
Status: Accepted

**Context:** The platform stores services, incidents, timeline events, alerts and RCA drafts. These are linked to each other (a service has incidents, an incident has events, alerts and drafts), and the core features depend on the data staying correct when requests arrive at the same time.

**Decision:** Use PostgreSQL 16.

**Why:**
- The data is relational. Foreign keys guarantee that an incident always belongs to a real service and an event to a real incident.
- Deduplication needs database-level guarantees: a partial unique index on `(service_id, fingerprint) WHERE status = 'firing'` with `INSERT … ON CONFLICT DO UPDATE`.
- A status change and its timeline event must be saved together, which needs transactions across tables.
- `CHECK` constraints keep status and severity values valid even if application code has a bug.
- MTTA/MTTR analytics need SQL: joins, CTEs, window functions, percentiles, and `EXPLAIN ANALYZE` for tuning.
- JSONB still gives schema flexibility where it's useful (event payloads, RCA draft content).

**Trade-offs:** Schema changes need migrations (handled with Alembic). Horizontal scaling is harder than with MongoDB, which is not a concern at this project's scale.

---

## ADR-002: Async SQLAlchemy 2.0 + asyncpg
Date: 2026-10-04
Status: Accepted

**Context:** The API is built with FastAPI, which is async. Most of a request's time is spent waiting on I/O: the database, and later the LLM API.

**Decision:** Use SQLAlchemy 2.0 in async mode with the asyncpg driver, and Alembic for migrations.

**Why:**
- With an async driver, one process can serve other requests while a query is waiting, instead of blocking.
- asyncpg is a fast, widely used async Postgres driver.
- SQLAlchemy 2.0 gives typed models, sessions and transactions, and works with Alembic for versioned, reversible migrations.
- Raw SQL is still available for analytics queries where hand-written SQL is clearer.

**Trade-offs:** Async adds complexity: lazy loading of relationships doesn't work implicitly, so related data must be loaded explicitly, and any blocking call inside an async function stalls every request. Tests need pytest-asyncio.
