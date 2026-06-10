# Contributing

Thanks for improving Agentic Systems Lab. This project is both a book and a runnable Python lab, so changes should preserve both reader clarity and reproducibility.

## Good Contributions

- Fix typos, broken links, unclear explanations, or formatting issues.
- Report or fix commands that no longer reproduce locally.
- Improve tests, fixtures, schemas, reports, or examples.
- Suggest focused extensions that preserve the deterministic core path.

## Evidence Standard

Non-trivial factual, vendor-specific, performance, and safety claims should be backed by at least one of:

- a primary source;
- a reproducible repo artifact;
- a local measurement;
- clearly labeled author interpretation.

Avoid adding unsupported certainty. If a claim is provisional, label it clearly or open an issue instead of burying a TODO in prose.

## Local Checks

Run the narrowest relevant checks while editing, then run the full check before opening a substantial pull request:

```bash
make check
```

This runs tests, examples, and HTML rendering.

## Pull Requests

Keep pull requests focused. Include:

- the problem being fixed;
- the files or chapters affected;
- the checks you ran;
- screenshots or rendered-page notes for visual book changes when useful.

For manuscript-only edits, run `make html`. If the prose references commands, schemas, sample output, or generated reports, also run the corresponding command or test.
