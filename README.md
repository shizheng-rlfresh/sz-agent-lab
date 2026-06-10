[![Agentic Systems Lab badge](assets/agent-47-badge.svg)](https://shizheng-rlfresh.github.io/sz-agent-lab/)

A hands-on HTML book and deterministic Python lab for learning how to build, trace, evaluate, harden, and reason about agentic AI systems.

**Read the book:** [https://shizheng-rlfresh.github.io/sz-agent-lab/](https://shizheng-rlfresh.github.io/sz-agent-lab/)

## About The Book

Agentic Systems Lab is written for technical readers who can read Python, reason about ML systems tradeoffs, and want a practical path from small deterministic fixtures to production-grade agent boundaries.

The book's thesis is that useful agent systems are not magic loops around an LLM. They are engineered runtimes with explicit tools, state boundaries, trace contracts, evals, guardrails, cost models, and rollout gates.

The style is concrete: each idea is tied to a runnable lab artifact, a command, a schema, or a production-readiness question.

Author: Zheng Shi, <shi.zheng.tfls@gmail.com>

Errata and clarification requests: [https://github.com/shizheng-rlfresh/sz-agent-lab/issues](https://github.com/shizheng-rlfresh/sz-agent-lab/issues)

## What You Will Learn

- How to separate deterministic workflows from agent-shaped runtime decisions.
- How to design tools, state boundaries, path confinement, and output caps.
- How to capture traces that explain what an agent actually did.
- How to write deterministic evals before reaching for model-judge evals.
- How guardrails and tool policy become runtime safety infrastructure.
- How context growth, token accounting, and cacheability shape agent cost.
- How local inference constraints change design choices.
- How to define production-readiness gates before automation reaches users.

## Book Contents

1. From LLM Calls to Agentic Systems
2. Workflows Before Agents
3. Designing Tools
4. State, Memory, and Context
5. Building the Repo Triage Agent
6. Tracing: From Transcript to Runtime Evidence
7. Evaluating Agents
8. Reports and Production-Readiness Evidence
9. Guardrails and Tool Policy
10. Prompt Injection and Untrusted Tool Output
11. Context, Cost, and Inference Bottlenecks
12. Prompt Caching and Prefix Stability
13. Local Agents and MLX
14. Production Readiness
15. Capstone: From Toy Agent to AgentProbe

Technical appendices cover further reading, glossary terms, command references, trace schemas, eval schemas, tool policy schemas, and the evidence/reference policy.

## Use The Lab

The core examples require no API keys. With `uv`, run the baseline checks and render the HTML book locally:

```bash
uv sync --extra dev
uv run pytest
uv run python scripts/run_all_examples.py
make html
```

For complete build, module, example, troubleshooting, and artifact commands, see the [command reference](appendices/command-reference.qmd). For contribution workflow expectations, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Project Links

- HTML book: [https://shizheng-rlfresh.github.io/sz-agent-lab/](https://shizheng-rlfresh.github.io/sz-agent-lab/)
- Issues and errata: [https://github.com/shizheng-rlfresh/sz-agent-lab/issues](https://github.com/shizheng-rlfresh/sz-agent-lab/issues)
- Build status: [https://github.com/shizheng-rlfresh/sz-agent-lab/actions/workflows/book.yml](https://github.com/shizheng-rlfresh/sz-agent-lab/actions/workflows/book.yml)
- License: [MIT](LICENSE)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- Command reference: [appendices/command-reference.qmd](appendices/command-reference.qmd)

## Roadmap

- Broaden the lab with richer eval task sets and sharper production evidence.
- Add trace export examples that map the local schema to common observability shapes.
- Keep optional hosted-model and local-inference paths clearly separated from the deterministic core.
- Grow the strongest follow-up into a focused OSS project around agent evaluation, cache stability, local readiness, or tool safety.
