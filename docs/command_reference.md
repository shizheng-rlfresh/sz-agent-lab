# Command Reference

## Core Verification

```bash
uv sync
uv run pytest
uv run scripts/run_all_examples.py
make html
```

Run these commands in this order when preparing a release or publishing the HTML book.

## Book Build Commands

```bash
make preview
make html
make clean
make test
make examples
make book
make check

```

`make preview` runs `quarto preview` for local reading while editing.

`make html` runs `quarto render --to html --no-clean` and produces `_book/index.html`.

`make clean` removes generated book output and local cache directories.

`make test` runs the test suite.

`make examples` runs all example scripts.

`make book` is an alias for the HTML book render.

`make check` runs tests, deterministic examples, and the HTML book render.

## Module Commands

```bash
uv run -m agentic_systems_lab.tools
uv run -m agentic_systems_lab.policy
uv run -m agentic_systems_lab.tracer
uv run -m agentic_systems_lab.agent
uv run -m agentic_systems_lab.evals
uv run -m agentic_systems_lab.context
uv run -m agentic_systems_lab.context --cache-demo
uv run -m agentic_systems_lab.report
```

These commands are intentionally small. Each module should be executable on its own so a reader can inspect behavior without running the entire book toolchain.

| Command | Primary Evidence | Expected Use |
|---|---|---|
| `uv run -m agentic_systems_lab.tools` | deterministic file listing, capped read, grep output | inspect read-only tool semantics |
| `uv run -m agentic_systems_lab.policy` | serialized default `ToolPolicy` | inspect runtime capability boundary |
| `uv run -m agentic_systems_lab.tracer` | sample trace summary | inspect JSONL trace writer and summarizer |
| `uv run -m agentic_systems_lab.agent` | structured repo-triage JSON | inspect deterministic agent output |
| `uv run -m agentic_systems_lab.evals` | default eval report | inspect pass/fail checks across fixtures |
| `uv run -m agentic_systems_lab.context` | context-profile summary | inspect token estimates and warnings |
| `uv run -m agentic_systems_lab.context --cache-demo` | prefix-stability comparison | inspect cacheable and dynamic prompt segments |
| `uv run -m agentic_systems_lab.report` | production report Markdown | inspect release-review artifact |

When documenting a chapter command, prefer one of these module commands over an ad hoc script. A public command is part of the book's reproducibility contract.

## Example Selection

```bash
uv run scripts/run_all_examples.py --example workflow_baseline
uv run scripts/run_all_examples.py --example repo_triage_agent
```

`scripts/run_all_examples.py` supports focused runs for development and full runs for release verification. Focused runs are useful while editing one chapter because they reduce feedback time. Full runs are required before committing changes that touch reports, schemas, fixture repos, or code paths shared by multiple chapters.

The examples are deliberately deterministic. If an example begins depending on current time, random UUIDs, network calls, local credentials, or model availability, it no longer belongs in the default acceptance path.

## Generated Artifacts

- `traces/buggy_calc_trace.jsonl`
- `reports/sample_trace_report.md`
- `reports/sample_eval_report.md`
- `reports/sample_production_report.md`
- `_book/index.html`

Generated artifacts fall into two categories. Runtime artifacts such as traces can contain local latency or timestamps, but committed sample reports should be stable. Book artifacts under `_book/` prove renderability but are not the source manuscript. When a generated artifact changes unexpectedly, ask which category it belongs to before deciding whether to commit it.

Review generated reports as evidence summaries, not as replacement sources of truth. A production report should link back to trace, eval, policy, and context artifacts. If a summary and raw artifact disagree, treat that as a report-generation defect.

## Optional MLX Command for Local LLM Inference (Working in Progress)

```bash
uv sync --extra apple-silicon
uv run mlx_lm.generate --model mlx-community/Llama-3.2-3B-Instruct-4bit --prompt "Explain AI Agent in simple terms."
```

Optional local-inference commands should never be required to run `pytest`, `python scripts/run_all_examples.py`, or `quarto render`. A reader without MLX-compatible hardware should still be able to complete the deterministic lab. If executable MLX support is added later, it should be behind an explicit optional dependency and an explicit command that can fail with a clear unavailable status.

## Verification

The repository's final acceptance path should run:

```bash
make check
```