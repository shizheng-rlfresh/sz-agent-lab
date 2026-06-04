# Agentic Systems Lab

A hands-on Quarto book and deterministic Python lab for learning how to build, trace, evaluate, harden, and reason about agentic AI systems.

This repository is written for a highly technical reader. It assumes you can read Python, reason about ML systems tradeoffs, and move quickly from a small fixture to the production boundary it represents.

The current book is organized as 15 chapters plus technical appendices. Its evidence standard is explicit: non-trivial claims should be backed by primary sources, reproducible repo artifacts, or clearly labeled author interpretation.

## What You Will Learn

- Workflows vs agents, with deterministic control flow before autonomy.
- Tool design, state boundaries, path confinement, and output caps.
- Trace contracts for agent runs.
- Deterministic evals before model-judge evals.
- Guardrails and tool policy as runtime safety infrastructure.
- Context growth, rough token accounting, and cacheability.
- Prompt/prefix cache stability.
- Local inference constraints: model size, context length, KV cache, memory pressure.
- Production-readiness gates for agentic systems.

## Quickstart

On a machine with only `python3` available:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
python scripts/run_all_examples.py
make html
make pdf
```

With `uv`:

```bash
uv run --extra dev pytest
uv run python scripts/run_all_examples.py
make html
make pdf
```

Book build targets:

```bash
make html   # render _book/index.html
make pdf    # render _book/Agentic-Systems-Lab.pdf
make book   # render both HTML and PDF
make check  # run tests, examples, and both book renders
```

PDF rendering uses Quarto's native PDF/LaTeX pipeline and requires a working PDF toolchain such as TinyTeX.

## Learning Path

1. Read Chapter 1 for the operational definition of an agentic system.
2. Run the workflow baseline to establish the deterministic floor.
3. Run the repo triage agent and inspect its JSON result.
4. Inspect the JSONL trace and generated trace report.
5. Run deterministic evals and inspect failure dimensions.
6. Review tool policy behavior against path traversal and shell access.
7. Profile context growth with the noisy log fixture.
8. Run the prompt-cache layout demo.
9. Generate the production report and identify missing rollout gates.
10. Use the capstone scorecard to choose a sharper OSS follow-up.

## Commands

```bash
python -m agentic_systems_lab.tools
python -m agentic_systems_lab.policy
python -m agentic_systems_lab.tracer
python -m agentic_systems_lab.agent
python -m agentic_systems_lab.evals
python -m agentic_systems_lab.context
python -m agentic_systems_lab.context --cache-demo
python -m agentic_systems_lab.report
python scripts/run_all_examples.py
```

## Repository Map

- `src/agentic_systems_lab/`: deterministic tools, policy, tracer, agent, evals, context profiler, and report generator.
- `data/toy_repos/`: small repos that encode concrete failure modes.
- `tests/`: behavior contracts for the core runtime.
- `reports/`: sample trace, eval, and production-readiness artifacts.
- `chapters/`: 15 Quarto book chapters that map concepts to code and artifacts.
- `appendices/`: glossary, command reference, schemas, policy reference, and evidence policy.
- `examples/`: command-oriented entry points for the learning path.

## Design Constraints

- Core examples require no API keys.
- Shell execution is disabled by default.
- Tools are read-only and path-confined.
- Numbers are estimates unless explicitly produced by local execution.
- Optional MLX content is documentation-only in the core path.

## Roadmap

- Add richer eval task sets beyond the current three toy failure modes.
- Add OpenTelemetry-shaped trace export.
- Add optional hosted-model and MLX adapters behind explicit feature gates.
- Split the strongest follow-up into a focused OSS project: `agentprobe`, `cachepilot`, `agentfit-mlx`, or `toolguard`.
