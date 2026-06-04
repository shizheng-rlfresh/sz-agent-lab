# Agentic Systems Lab — Real Book Expansion Plan

## Purpose

Turn the current runnable Quarto/code scaffold into a real technical book: evidence-backed, production-shaped, and useful to a fast senior/staff-level ML engineer.

## Decisive Evidence Standard

Every non-trivial factual, technical, historical, vendor-specific, performance-related, or safety-related statement must be supported by one of:

1. a cited primary or authoritative source,
2. a reproducible result from this repository,
3. a clearly labeled author interpretation,
4. a clearly labeled hypothesis.

Unsupported claims should be removed, softened, or rewritten as questions.

## Book Thesis

A model call is not an agentic system. An agentic system becomes production-shaped when it has explicit tool boundaries, state discipline, traceability, evals, guardrails, context control, cost and latency awareness, rollout gates, and rollback discipline.

## Full Structure

- Part I — Foundations
  - Chapter 1 — From LLM Calls to Agentic Systems
  - Chapter 2 — Workflows Before Agents
- Part II — Tools, State, and Runtime
  - Chapter 3 — Designing Tools
  - Chapter 4 — State, Memory, and Context
  - Chapter 5 — Building the Repo Triage Agent
- Part III — Measurement
  - Chapter 6 — Tracing: From Transcript to Runtime Evidence
  - Chapter 7 — Evaluating Agents
  - Chapter 8 — Reports and Production-Readiness Evidence
- Part IV — Safety and Hardening
  - Chapter 9 — Guardrails and Tool Policy
  - Chapter 10 — Prompt Injection and Untrusted Tool Output
- Part V — Infra and Cost
  - Chapter 11 — Context, Cost, and Inference Bottlenecks
  - Chapter 12 — Prompt Caching and Prefix Stability
  - Chapter 13 — Local Agents and MLX
- Part VI — Deployment and Capstone
  - Chapter 14 — Production Readiness
  - Chapter 15 — Capstone: From Toy Agent to AgentProbe
- Appendices
  - Appendix A — Glossary
  - Appendix B — Command Reference
  - Appendix C — Trace Schema
  - Appendix D — Eval Schema
  - Appendix E — Tool Policy Schema
  - Appendix F — Evidence and Reference Policy

## Chapter Template

Each chapter should normally include:

- Learning Objective
- Why This Matters
- Core Concept
- The Lab
- Code Walkthrough
- Expected Output
- Failure Mode
- Production Translation
- Evidence and References
- Exercises
- Checklist

## Milestones

1. Expansion scaffold: book structure, appendices, render succeeds.
2. Foundations and runtime chapters.
3. Measurement and safety chapters.
4. Infra, production, and capstone chapters.
5. Appendices and reference quality.
6. Editorial pass with tests, examples, and Quarto render.
