# Engineering diary

## Oct 1 — Restart and rescope

What I built:
Re-cloned the repo on a new machine, installed uv and Docker, and verified it from a clean state (uv sync, pytest, docker compose, alembic upgrade head).
Rescoped and rewrote the README.

Decision + why:
Fixed the July foundation instead of starting over. The stack was right; only
config and scope were wrong. Rescoped from "RCA & Runbook Generator" to
"Incident & RCA Platform" so the core is FastAPI + PostgreSQL design, with the
LLM as one feature on top.

What broke / what surprised me:
A fresh clone couldn't start. .env is gitignored, .env.example was missing the POSTGRES_* vars docker-compose needs, and DATABASE_URL used the in-network hostname "postgres" instead of localhost. 
"Day 1 done" in July had only ever been tested on the machine it was written on.

What I'd do differently:
Test from a fresh clone (or CI) before calling anything done.

Interview soundbite:
"My definition of done is that it runs from a fresh clone. The first time I
actually tested that, it failed, and that's now a rule."