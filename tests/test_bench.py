from fliorcie_bench.render import render_markdown
from fliorcie_bench.runner import run_demo_benchmark


def test_demo_benchmark_record_is_evidence_shaped() -> None:
    record = run_demo_benchmark(iterations=5)

    assert record.schema_version == "fl-bench-record-v0.1"
    assert record.passed
    assert record.mean_us >= 0
    assert record.p95_us >= 0
    assert "not a universal performance claim" in " ".join(record.limitations)


def test_markdown_report_includes_limitations() -> None:
    record = run_demo_benchmark(iterations=2).to_dict()
    markdown = render_markdown(record)

    assert "# FL-BENCH Local Benchmark Report" in markdown
    assert "Limitations" in markdown
    assert "universal performance claim" in markdown
