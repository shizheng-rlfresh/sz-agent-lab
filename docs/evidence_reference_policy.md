# Evidence and Reference Policy

## Citation Standard

Every non-trivial factual, technical, vendor-specific, performance-related, or safety-related statement in this book should be backed by one of:

1. **Documented fact**: cite an authoritative source.
2. **Repo-observed behavior**: cite a runnable command and expected output.
3. **Author interpretation**: label it as interpretation or design judgment.
4. **Hypothesis**: label it as a hypothesis.
5. **Measurement**: include method, environment, and limitations.

This policy is intentionally strict because the intended reader can already detect vague claims. The book should not trade on agent excitement. It should make narrow claims and show why they are defensible.

When a claim cannot be supported, either remove it, narrow it, or mark it as a TODO. Unsupported certainty is worse than an explicit gap.

## Preferred Source Hierarchy

1. Primary documentation from the technology owner.
2. Peer-reviewed or widely cited research papers.
3. Official engineering blogs from reputable organizations.
4. Well-maintained open-source documentation.
5. Secondary explainers only when clearly labeled.

Primary sources are especially important for vendor-specific behavior such as prompt caching, SDK tracing, or MLX commands. These behaviors can change over time. A secondary blog may be useful for intuition, but it should not be the only source for an operational claim.

Research papers are appropriate for inference mechanisms and algorithms, but be careful about scope. A paper's benchmark result does not automatically imply the same result in this repo, on this hardware, or under this workload.

## Examples of Supported Claims

- "The local eval suite checks `buggy_calc`, `prompt_injection_repo`, and `noisy_logs_repo`." Supported by `python -m agentic_systems_lab.evals`.
- "OpenAI prompt caching depends on exact prefix matches." Supported by OpenAI prompt caching docs [@openai_prompt_caching].
- "KV-cache memory is an inference concern." Supported by Hugging Face documentation and PagedAttention [@huggingface_kv_cache; @pagedattention].

More examples:

- "The book renders as a Quarto book." Supported by `quarto render` and the Quarto book documentation [@quarto_book_docs].
- "The default tool policy blocks shell execution." Supported by `tests/test_policy.py` and `python -m agentic_systems_lab.policy`.
- "Prompt-injection risk is a recognized LLM application security concern." Supported by OWASP [@owasp_llm_top10].
- "The local cache demo estimates stable and dynamic prompt segments." Supported by `python -m agentic_systems_lab.context --cache-demo`.

## Prohibited Patterns

Avoid:

```text
Everyone knows...
It is obvious that...
Agents always...
This dramatically improves...
Modern systems require...
```

unless the claim is narrowed and supported.

Also avoid laundering opinion through passive voice:

```text
It is considered best practice to...
It has been shown that...
Production systems need...
The industry is moving toward...
```

These phrases often hide the missing source. Replace them with the actor, source, measurement, or local evidence.

## Preferred Patterns

Use:

```text
In this lab...
In this implementation...
Under this assumption...
Provider documentation states...
The cited paper reports...
Our local measurement shows...
A reasonable design interpretation is...
```

For design judgment, be explicit:

```text
This book treats read-only tools as the default because it makes the first safety boundary easy to inspect.
```

For local evidence, include the command:

```text
In this repo, `python -m agentic_systems_lab.evals` reports the default fixture outcomes.
```

For hypotheses, preserve uncertainty:

```text
A plausible next improvement is to summarize noisy logs before prompt assembly; this repo has not measured that variant.
```

## Local Measurement Rules

When reporting measurements:

- name the command,
- record hardware or runtime when relevant,
- distinguish estimates from exact counts,
- do not generalize from one local run to all deployments.

Measurement notes should include enough detail for a reader to reproduce or challenge the result. For context and inference measurements, record model, tokenizer if used, prompt size, completion size, hardware, batch shape if relevant, and whether caching was warm or cold.

If the code uses a crude token estimate, call it an estimate. Do not present it as provider tokenizer output.

## Editorial Review Checklist

For each chapter, check:

- Are vendor-specific claims cited?
- Are performance claims cited, measured, or labeled as estimates?
- Are security claims cited or demonstrated with fixtures?
- Are author judgments labeled as judgments?
- Does every lab command still run?
- Does the expected output match current artifacts?

For each reference, check:

- Does the citation support the sentence where it appears?
- Is the source primary or clearly justified?
- Is the cited behavior stable enough for a book claim?
- Does the bibliography entry include a useful URL or DOI?
- Are unresolved claims marked as TODO rather than silently asserted?

For each lab, check:

- Is there a deterministic command?
- Is expected output described at the right granularity?
- Is failure interpretation included?
- Are sample artifacts regenerated when behavior changes?
- Are optional dependencies clearly optional?

## Claim Rewriting Examples

Weak:

```text
Agents are unreliable in production.
```

Stronger:

```text
In this repo, a final answer without a trace is insufficient for review because it does not show which files were inspected.
```

Weak:

```text
Prompt caching dramatically reduces latency.
```

Stronger:

```text
Provider documentation describes prompt caching as an optimization for repeated prefixes; this repo only demonstrates static prefix-stability analysis.
```

Weak:

```text
Local models are cheaper.
```

Stronger:

```text
Local inference can make marginal API spend predictable, but total cost depends on hardware, utilization, operations, quality, and workload. This repo treats MLX as optional and does not benchmark local cost.
```

Weak:

```text
Tracing makes agents safe.
```

Stronger:

```text
Tracing makes selected runtime behavior reviewable. It does not by itself enforce policy or prove task correctness.
```

Weak:

```text
The agent found the bug.
```

Stronger:

```text
The deterministic agent reported the division-by-zero contract mismatch after inspecting `calculator.py` and `test_calculator.py`, as shown by the generated trace and eval report.
```

## TODO Discipline

Use explicit TODO markers for unresolved support:

```text
TODO: find primary source for provider-specific cache threshold before making this claim.
```

A TODO is acceptable in a draft, but it should not survive final verification for a central claim. Peripheral TODOs should be listed in the expansion plan or issue tracker rather than buried in prose.

## Evidence Types by Chapter

Use different evidence types where they fit:

- Foundations: authoritative agent/workflow guidance plus local design definitions.
- Tools and policy: local tests, fixture behavior, and OWASP risk framing.
- Tracing: local JSONL traces plus OpenAI and OpenTelemetry documentation.
- Evals and reports: local generated artifacts plus NIST risk-management framing.
- Context and caching: local token estimates plus provider and inference-runtime documentation.
- MLX: official MLX/MLX-LM documentation, with executable behavior kept optional.
- Capstone: repo artifacts and clearly labeled author interpretation.

This mapping prevents accidental over-citation and accidental under-citation. Not every sentence needs a citation, but every external or performance-sensitive claim needs support.

## Final Evidence Audit

Before publishing, run a final audit:

1. Search for broad claims such as "always," "never," "dramatically," "best," and "production systems require."
2. For each result, either cite a source, narrow the claim, or label it as author judgment.
3. Run every command named in the command reference.
4. Confirm sample reports match generated behavior.
5. Confirm optional MLX language remains optional.
6. Confirm every TODO is either resolved or intentionally listed as future work.

This audit is intentionally mechanical. Mechanical checks catch the kinds of unsupported certainty that technical authors often miss after spending too much time inside a draft.
