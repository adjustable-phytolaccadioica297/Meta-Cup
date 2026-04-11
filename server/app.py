from __future__ import annotations

import os
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse

from models import (
    Action,
    GradeRequest,
    GraderResult,
    InternalStateSnapshot,
    Observation,
    ResetRequest,
    ScenarioSummary,
    StepResult,
)
from server.environment import RunbookOpsEnvironment

app = FastAPI(
    title="RunbookOps API",
    description="Deterministic operational case handling benchmark for evidence-based triage and safe resolution",
    version="0.1.0",
)

env = RunbookOpsEnvironment()


def _root_payload() -> dict[str, object]:
    return {
        "name": "RunbookOps",
        "status": "ok",
        "tagline": "CaseOps benchmark for operational case handling",
        "docs": "/docs",
        "health": "/health",
    }


def _landing_page_html() -> str:
    difficulty_counts = env.list_tasks()
    total_scenarios = len(env.scenarios)
    easy_count = difficulty_counts["easy"]["scenario_count"]
    medium_count = difficulty_counts["medium"]["scenario_count"]
    hard_count = difficulty_counts["hard"]["scenario_count"]
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>RunbookOps - CaseOps Benchmark</title>
    <style>
      :root {{
        --canvas: #efe4d4;
        --canvas-deep: #e0d0b8;
        --paper: rgba(255, 251, 244, 0.9);
        --paper-strong: #fffaf3;
        --ink: #201b18;
        --ink-soft: #5f564f;
        --line: rgba(69, 56, 47, 0.14);
        --rail: #243041;
        --rail-soft: #314155;
        --cream: #fff6e7;
        --accent: #b95b38;
        --accent-dark: #8f4428;
        --teal: #2f6b64;
        --gold: #b88a2b;
        --success: #83c589;
      }}
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        min-height: 100vh;
        color: var(--ink);
        background:
          radial-gradient(circle at top right, rgba(185, 91, 56, 0.12), transparent 34%),
          radial-gradient(circle at left 20%, rgba(47, 107, 100, 0.1), transparent 28%),
          linear-gradient(180deg, var(--canvas) 0%, #eadfcd 48%, var(--canvas-deep) 100%);
        font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }}
      a {{ color: inherit; text-decoration: none; }}
      .shell {{
        width: min(1180px, calc(100vw - 32px));
        margin: 0 auto;
        padding: 32px 0 56px;
      }}
      .masthead {{
        display: grid;
        grid-template-columns: minmax(0, 1.45fr) minmax(320px, 0.9fr);
        gap: 22px;
        align-items: stretch;
      }}
      .panel {{
        border-radius: 34px;
        border: 1px solid var(--line);
        box-shadow: 0 28px 72px rgba(62, 43, 27, 0.14);
      }}
      .hero {{
        position: relative;
        overflow: hidden;
        background:
          linear-gradient(145deg, rgba(255, 251, 244, 0.95) 0%, rgba(248, 240, 229, 0.9) 100%);
      }}
      .hero::before {{
        content: "";
        position: absolute;
        inset: 0;
        background:
          linear-gradient(90deg, rgba(47, 107, 100, 0.06), transparent 30%),
          linear-gradient(0deg, rgba(185, 91, 56, 0.05), transparent 40%);
        pointer-events: none;
      }}
      .hero-copy {{
        position: relative;
        padding: 38px 38px 34px;
      }}
      .hero-topline {{
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        align-items: center;
      }}
      .eyebrow {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        border-radius: 999px;
        background: rgba(47, 107, 100, 0.1);
        border: 1px solid rgba(47, 107, 100, 0.16);
        color: var(--teal);
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
      }}
      .eyebrow.warm {{
        background: rgba(185, 91, 56, 0.1);
        border-color: rgba(185, 91, 56, 0.16);
        color: var(--accent);
      }}
      .project-kicker {{
        margin: 18px 0 10px;
        color: var(--ink-soft);
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
      }}
      h1 {{
        margin: 0;
        max-width: 10ch;
        font-family: "Iowan Old Style", "Palatino Linotype", "Book Antiqua", Georgia, serif;
        font-size: clamp(42px, 6vw, 76px);
        line-height: 0.92;
        letter-spacing: -0.05em;
        color: #171311;
      }}
      .lede {{
        max-width: 64ch;
        margin: 18px 0 0;
        color: var(--ink-soft);
        font-size: 18px;
        line-height: 1.7;
      }}
      .lede strong {{
        color: var(--ink);
      }}
      .cta-row {{
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin: 26px 0 30px;
      }}
      .button {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        min-width: 150px;
        padding: 14px 18px;
        border-radius: 999px;
        font-weight: 800;
        border: 1px solid var(--line);
      }}
      .button.primary {{
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-dark) 100%);
        border-color: rgba(143, 68, 40, 0.18);
        color: var(--cream);
      }}
      .button.secondary {{
        background: rgba(36, 48, 65, 0.06);
        color: var(--ink);
      }}
      .button.ghost {{
        background: transparent;
        color: var(--ink-soft);
      }}
      .metrics {{
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 12px;
      }}
      .metric {{
        padding: 18px 16px 16px;
        border-radius: 22px;
        background: rgba(255, 250, 243, 0.85);
        border: 1px solid rgba(69, 56, 47, 0.1);
      }}
      .metric .value {{
        font-size: 34px;
        font-weight: 800;
        letter-spacing: -0.04em;
      }}
      .metric .label {{
        margin-top: 4px;
        color: var(--ink-soft);
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
      }}
      .caseboard {{
        position: relative;
        overflow: hidden;
        background:
          radial-gradient(circle at top right, rgba(184, 138, 43, 0.16), transparent 24%),
          linear-gradient(180deg, var(--rail) 0%, #18222e 100%);
        color: #f0efe9;
        padding: 28px;
        display: flex;
        flex-direction: column;
        gap: 16px;
      }}
      .caseboard::after {{
        content: "";
        position: absolute;
        inset: auto 24px 20px auto;
        width: 96px;
        height: 96px;
        border-radius: 28px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        transform: rotate(8deg);
        pointer-events: none;
      }}
      .badge {{
        display: inline-flex;
        width: fit-content;
        padding: 7px 11px;
        border-radius: 999px;
        background: rgba(131, 197, 137, 0.14);
        border: 1px solid rgba(131, 197, 137, 0.22);
        color: #dff2e0;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
      }}
      .card-title {{
        margin: 0;
        font-family: "Iowan Old Style", "Palatino Linotype", Georgia, serif;
        font-size: 31px;
        font-weight: 800;
        line-height: 1.04;
      }}
      .bullet-list {{
        margin: 0;
        padding-left: 18px;
        color: rgba(240, 239, 233, 0.84);
        line-height: 1.7;
      }}
      .route-list {{
        margin-top: 12px;
        display: grid;
        gap: 10px;
      }}
      .route {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        padding: 13px 14px;
        border-radius: 18px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
      }}
      .route code {{
        color: #9de4d6;
        font-size: 13px;
        font-weight: 700;
      }}
      .route span {{
        color: rgba(240, 239, 233, 0.7);
        font-size: 13px;
      }}
      .surface {{
        margin-top: 24px;
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 16px;
      }}
      .surface-card {{
        padding: 22px 22px 24px;
        background: rgba(255, 249, 241, 0.86);
      }}
      .surface-card h3 {{
        margin: 0 0 12px;
        font-size: 18px;
        letter-spacing: -0.02em;
      }}
      .surface-card p {{
        margin: 0;
        color: var(--ink-soft);
        line-height: 1.72;
        font-size: 14px;
      }}
      .surface-card .small-label {{
        display: inline-block;
        margin-bottom: 12px;
        color: var(--gold);
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.1em;
        text-transform: uppercase;
      }}
      @media (max-width: 980px) {{
        .masthead, .surface {{
          grid-template-columns: 1fr;
        }}
        .metrics {{
          grid-template-columns: repeat(2, minmax(0, 1fr));
        }}
      }}
      @media (max-width: 640px) {{
        .shell {{
          width: min(100vw - 20px, 1180px);
          padding-top: 20px;
        }}
        .hero-copy, .caseboard, .surface-card {{
          padding: 22px;
        }}
        .metrics {{
          grid-template-columns: 1fr 1fr;
        }}
        h1 {{
          max-width: none;
        }}
      }}
    </style>
  </head>
  <body>
    <main class="shell">
      <section class="masthead">
        <div class="panel hero">
          <div class="hero-copy">
            <div class="hero-topline">
              <div class="eyebrow">OpenEnv RL Challenge</div>
              <div class="eyebrow warm">Deterministic and offline</div>
            </div>
            <p class="project-kicker">RunbookOps / CaseOps Benchmark</p>
            <h1>Operational case handling for agents that need to earn the close.</h1>
          <p class="lede">
            <strong>RunbookOps</strong> turns real operational work into a deterministic benchmark.
            Agents must gather evidence, classify impact, route ownership, diagnose the issue,
            choose a safe resolution, and close customer-facing cases without shallow shortcuts.
          </p>
          <div class="cta-row">
            <a class="button primary" href="/docs">Open API Docs</a>
            <a class="button secondary" href="/scenarios">Browse Scenarios</a>
            <a class="button ghost" href="/health">Health Check</a>
          </div>
          <div class="metrics">
            <div class="metric">
              <div class="value">{total_scenarios}</div>
              <div class="label">total cases</div>
            </div>
            <div class="metric">
              <div class="value">{easy_count}</div>
              <div class="label">easy</div>
            </div>
            <div class="metric">
              <div class="value">{medium_count}</div>
              <div class="label">medium</div>
            </div>
            <div class="metric">
              <div class="value">{hard_count}</div>
              <div class="label">hard</div>
            </div>
          </div>
        </div>
        </div>
        <aside class="panel caseboard">
          <div class="badge">Deterministic and Offline</div>
          <h2 class="card-title">Why judges and builders can trust this benchmark</h2>
          <ul class="bullet-list">
            <li>Real operational work instead of a toy game loop</li>
            <li>No LLM-as-judge scoring or hidden internet dependencies</li>
            <li>Evidence, routing, diagnosis, and safe closure all matter</li>
            <li>Continuous deterministic grading with meaningful score variance</li>
          </ul>
          <div class="route-list">
            <a class="route" href="/reset"><code>POST /reset</code><span>start a case</span></a>
            <a class="route" href="/step"><code>POST /step</code><span>advance one action</span></a>
            <a class="route" href="/grade"><code>POST /grade</code><span>score current episode</span></a>
            <a class="route" href="/tasks"><code>GET /tasks</code><span>list task groups</span></a>
          </div>
        </aside>
      </section>

      <section class="surface">
        <article class="panel surface-card">
          <span class="small-label">Evidence first</span>
          <h3>Evidence-Based Resolution</h3>
          <p>
            Cases expose alerts, logs, workflow playbooks, and timeline notes gradually. The
            agent must collect enough evidence before proposing cause and mitigation.
          </p>
        </article>
        <article class="panel surface-card">
          <span class="small-label">Built for review</span>
          <h3>Judge-Friendly Structure</h3>
          <p>
            Typed models, FastAPI endpoints, Docker deployment, deterministic grading, and a
            baseline inference runner aligned with the OpenEnv submission contract.
          </p>
        </article>
        <article class="panel surface-card">
          <span class="small-label">Broader audience</span>
          <h3>Broader Than Infra Ops</h3>
          <p>
            RunbookOps is framed as operational case handling across access failures, order issues,
            payment exceptions, message delivery, search freshness, and integration regressions.
          </p>
        </article>
      </section>
    </main>
  </body>
</html>"""


@app.get("/", response_model=None)
def root(request: Request):
    accepts = request.headers.get("accept", "")
    if "application/json" in accepts:
        return JSONResponse(_root_payload())
    return HTMLResponse(_landing_page_html())


@app.get("/health")
def health() -> dict[str, object]:
    return {
        "status": "ok",
        "environment": "RunbookOps",
        "scenarios_loaded": len(env.scenarios),
    }


@app.post("/reset", response_model=Observation)
def reset(request: Optional[ResetRequest] = None) -> Observation:
    request = request or ResetRequest()
    try:
        return env.reset(scenario_id=request.scenario_id, difficulty=request.difficulty)
    except (RuntimeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/step", response_model=StepResult)
def step(action: Action) -> StepResult:
    try:
        return env.step(action)
    except (RuntimeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/state", response_model=InternalStateSnapshot)
def state() -> InternalStateSnapshot:
    try:
        return env.state()
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/tasks")
def tasks() -> dict[str, dict[str, object]]:
    return env.list_tasks()


@app.get("/scenarios", response_model=list[ScenarioSummary])
def scenarios() -> list[ScenarioSummary]:
    return env.list_scenarios()


@app.post("/grade", response_model=GraderResult)
def grade(request: Optional[GradeRequest] = None) -> GraderResult:
    request = request or GradeRequest()
    try:
        if request.scenario_id and env.state().scenario_id != request.scenario_id:
            raise ValueError(
                "Active scenario does not match scenario_id in request. Call /reset first."
            )
        return env.grade_current_episode()
    except (RuntimeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/score", response_model=GraderResult)
def score(request: Optional[GradeRequest] = None) -> GraderResult:
    return grade(request)


def main() -> None:
    import uvicorn

    uvicorn.run(
        "server.app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "7860")),
    )


if __name__ == "__main__":
    main()
