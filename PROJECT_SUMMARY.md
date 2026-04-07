# RunbookOps: Project Summary

## One-Line Summary

RunbookOps is a deterministic OpenEnv-style environment that evaluates whether an agent can perform realistic SaaS incident triage and runbook-based resolution safely.

## Why It Matters

Incident response is a high-value real-world agent task with concrete success criteria. RunbookOps provides structured evaluation beyond toy environments by testing evidence-driven reasoning, ownership routing, mitigation choice, and safe closure behavior.

## What Is Included

- 15 fully synthetic, offline scenarios.
  - 5 easy, 5 medium, 5 hard.
- Typed action/observation/state models (Pydantic).
- Deterministic environment API:
  - `reset()`
  - `step(action)`
  - `state()`
- Deterministic rubric-based grader with validator-safe published score in `(0.0, 1.0)`.
- Dense trajectory reward with partial-progress signals.
- FastAPI server endpoints for local and container deployment.
- Baseline `inference.py` using OpenAI client and required env vars.
- Dockerfile and test suite.

## Judge Quick Path (2-3 minutes)

1. Start API and open `/docs`.
2. Call `POST /reset` with `easy_auth_token_expiry`.
3. Call `POST /step` with one inspect action, then `GET /state`.
4. Call `POST /grade` and verify score is in `[0, 1]`.
5. Run `python3 -m pytest` for deterministic validation coverage.

## Judging Alignment

- Real-world utility: incident triage and runbook operations.
- Task/grader quality: explicit objectives, deterministic grading, difficulty progression.
- Environment design: stateful evidence unlocking, safety-aware transitions, reward shaping.
- Spec-readiness: typed models, OpenEnv-style manifest, deployable API + Docker.

## Quick Verification

1. Open `/docs` and call `POST /reset`, `POST /step`, `GET /state`, `POST /grade`.
2. Run `pytest`.
3. Run `python3 scripts/smoke_test.py`.
4. Build/run Docker and verify `/health`.

## Key Files

- `server/environment.py`
- `grader.py`
- `openenv.yaml`
- `inference.py`
- `tests/`
