from __future__ import annotations


def render_markdown(record: dict[str, object]) -> str:
    dimensions = record.get("dimensions", [])
    lines = [
        f"# {record['component']} Local Benchmark Report",
        "",
        f"- Scenario: `{record['scenario_id']}`",
        f"- Run: `{record['run_id']}`",
        f"- Verdict: `{record['verdict']}`",
        f"- Passed: `{record['passed']}`",
        f"- Mean: `{float(record['mean_us']):.2f} us`",
        f"- P95: `{float(record['p95_us']):.2f} us`",
        "",
        "## Dimensions",
        "",
    ]
    for dimension in dimensions:
        item = dimension if isinstance(dimension, dict) else {}
        lines.append(
            f"- `{item.get('name')}`: `{item.get('passed')}` - {item.get('details')}"
        )
    lines.extend(
        [
            "",
            "## Limitations",
            "",
        ]
    )
    for limitation in record.get("limitations", []):
        lines.append(f"- {limitation}")
    lines.append("")
    return "\n".join(lines)

