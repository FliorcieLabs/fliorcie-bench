from __future__ import annotations

import json
import platform
import statistics
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path


class BenchVerdict(str, Enum):
    VERIFIED = "VERIFIED"
    FALSE = "FALSE"
    PARTIAL = "PARTIAL"
    UNVERIFIED = "UNVERIFIED"
    CONTRADICTORY = "CONTRADICTORY"
    UNAUTHORIZED = "UNAUTHORIZED"
    UNSAFE = "UNSAFE"
    COMPENSATION_REQUIRED = "COMPENSATION_REQUIRED"


@dataclass(frozen=True)
class BenchDimension:
    name: str
    passed: bool
    details: str


@dataclass(frozen=True)
class BenchEnvironment:
    python: str
    platform: str
    processor: str

    @classmethod
    def local(cls) -> "BenchEnvironment":
        return cls(
            python=platform.python_version(),
            platform=platform.platform(),
            processor=platform.processor() or "unknown",
        )


@dataclass(frozen=True)
class BenchRecord:
    schema_version: str
    component: str
    scenario_id: str
    run_id: str
    verdict: BenchVerdict
    dimensions: tuple[BenchDimension, ...]
    durations_us: tuple[float, ...]
    environment: BenchEnvironment
    limitations: tuple[str, ...] = field(default_factory=tuple)

    @property
    def mean_us(self) -> float:
        return statistics.fmean(self.durations_us) if self.durations_us else 0.0

    @property
    def p95_us(self) -> float:
        if not self.durations_us:
            return 0.0
        values = sorted(self.durations_us)
        index = min(len(values) - 1, int(round((len(values) - 1) * 0.95)))
        return values[index]

    @property
    def passed(self) -> bool:
        return self.verdict == BenchVerdict.VERIFIED and all(
            dimension.passed for dimension in self.dimensions
        )

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["verdict"] = self.verdict.value
        data["mean_us"] = self.mean_us
        data["p95_us"] = self.p95_us
        data["passed"] = self.passed
        return data


def write_record(path: Path, record: BenchRecord) -> None:
    path.write_text(json.dumps(record.to_dict(), indent=2, sort_keys=True), encoding="utf-8")


def read_record(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))

