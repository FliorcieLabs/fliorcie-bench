from __future__ import annotations

import time
import uuid

from .core import BenchDimension, BenchEnvironment, BenchRecord, BenchVerdict


def _measured_noop() -> None:
    sum(range(10))


def run_demo_benchmark(iterations: int = 100) -> BenchRecord:
    durations: list[float] = []
    for _ in range(iterations):
        start = time.perf_counter_ns()
        _measured_noop()
        durations.append((time.perf_counter_ns() - start) / 1000)

    return BenchRecord(
        schema_version="fl-bench-record-v0.1",
        component="FL-BENCH",
        scenario_id="FL-BENCH-DEMO-NOOP",
        run_id=str(uuid.uuid4()),
        verdict=BenchVerdict.VERIFIED,
        dimensions=(
            BenchDimension("deterministic-local-run", True, "no network or credentials"),
            BenchDimension("raw-secret-free-record", True, "record contains only metadata"),
        ),
        durations_us=tuple(durations),
        environment=BenchEnvironment.local(),
        limitations=(
            "demo workload only",
            "local machine timing is not a universal performance claim",
        ),
    )

