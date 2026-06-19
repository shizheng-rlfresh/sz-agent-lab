<br>

<p align="center">
    <img alt="Built with human review and Codex assistance" src="https://img.shields.io/badge/human--reviewed-Codex--assisted-412991?style=flat-square">
    <img alt="Version: v0.1.1" src="https://img.shields.io/badge/version-v0.1.1-blue?style=flat-square">
    <img alt="Book workflow status" src="https://github.com/shizheng-rlfresh/sz-agent-lab/actions/workflows/book.yml/badge.svg?branch=main" />
</p>

<p align="center">
  <a href="https://agent-book.zhengqxhs.com/">
    <img alt="Agentic Systems Lab badge" src="assets/agent-47-badge.svg" />
  </a>
</p>

A hands-on HTML book and deterministic Python lab for learning how to build, trace, evaluate, harden, and reason about agentic AI systems.

<hr>
<br>

📘 **Read the book:** [https://agent-book.zhengqxhs.com/](https://agent-book.zhengqxhs.com/)

<img src="assets/python.png" alt="Python" width="18" height="18"> **Run the lab:**

```bash
uv sync
uv run scripts/run_all_examples.py
```

**🔍 Inspect the evidence trail:** [sample trace report](reports/sample_trace_report.md), [sample eval report](reports/sample_eval_report.md), and [sample production report](reports/sample_production_report.md). Raw trace artifacts are generated under `traces/` after running `uv run scripts/run_all_examples.py`.

<br>

## About The Book

Agentic Systems Lab is written for technical readers who can read Python, reason about ML systems tradeoffs, and want a practical path from small deterministic fixtures to production-grade agent boundaries.

The book's thesis is that useful agent systems are not magic loops around an LLM. They are engineered runtimes with explicit tools, state boundaries, trace contracts, evals, guardrails, cost models, and rollout gates.

The style is concrete: each idea is tied to a runnable lab artifact, a command, a schema, or a production-readiness question.

## Why This Exists

Many agent tutorials start with a prompt loop and then add discipline after the behavior becomes hard to inspect. This lab takes the opposite path: deterministic workflows first, then tools, state, traces, evals, guardrails, context budgets, and deployment gates.

The core path requires no API key, hosted model provider, or cloud account. That keeps the runtime contracts visible before model variance enters the system.

The result is an evidence-first way to learn agentic systems: readers can inspect what ran, what was traced, what passed evaluation, and what would need to be true before automation reaches users.

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

Technical appendices cover further reading, trace schemas, eval schemas, tool policy schemas, and glossary terms.

## Development

The core examples require no API keys. With `uv`, run the baseline checks and render the HTML book locally:

```bash
uv sync
uv run pytest
uv run scripts/run_all_examples.py
make html
```

(Working in Progress) MLX for Local Dev on Apple Silicon

```bash
uv sync --extra apple-silicon # installs the optional apple-silicon extra (mlx-lm)
uv run mlx_lm.generate --model mlx-community/Llama-3.2-3B-Instruct-4bit --prompt "Explain AI Agent in simple terms."
```

For complete build, module, example, troubleshooting, and artifact commands, see the [command reference](docs/command_reference.md). For contribution workflow expectations, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Project Links

- Issues and errata: [https://github.com/shizheng-rlfresh/sz-agent-lab/issues](https://github.com/shizheng-rlfresh/sz-agent-lab/issues)
- Build status: [https://github.com/shizheng-rlfresh/sz-agent-lab/actions/workflows/book.yml](https://github.com/shizheng-rlfresh/sz-agent-lab/actions/workflows/book.yml)
- License: [MIT](LICENSE)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- Command reference: [command_reference.md](docs/command_reference.md)

## Citation

If you cite or share this project, use the repository title, author, public book URL, and the release tag or commit SHA for the version you used:

```text
Zheng Shi. Agentic Systems Lab: Building, Measuring, and Hardening AI Agents.
https://agent-book.zhengqxhs.com/
Version: release tag or commit SHA
```

## Roadmap

- Broaden the lab with richer eval task sets and sharper production evidence.
- Add trace export examples that map the local schema to common observability shapes.
- Keep optional hosted-model and local-inference paths clearly separated from the deterministic core.
- Grow the strongest follow-up into a focused OSS project around agent evaluation, cache stability, local readiness, or tool safety.
