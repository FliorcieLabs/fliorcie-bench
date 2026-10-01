# Fliorcie Bench

Local benchmark and conformance reporting for Fliorcie Community components.

The bench records reproducible local evidence: component, scenario, environment,
dimensions, timings, verdict, and limitations. It does not publish leaderboards,
claim universal performance, or train models.

## Boundary

- `FL-BENCH`: deterministic local benchmark records and Markdown/JSON reports.
- Bench reports are evidence, not marketing claims.
- Duration is recorded, but pass/fail should be based on semantic dimensions.
- Raw prompts, credentials, customer data, and artifact bytes should be replaced
  with hashes or omitted.

## Quick Start

```bash
python -m pip install -e .
python -m pytest
fl-bench demo --output local-bench.json
fl-bench render local-bench.json --output local-bench.md
```

