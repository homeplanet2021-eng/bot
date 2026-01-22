"""Minimal metrics registry (placeholder for Prometheus)."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Counter:
    name: str
    labels: tuple[str, ...] = ()
    _values: dict[tuple[str, ...], int] = field(default_factory=dict)

    def inc(self, label_values: tuple[str, ...] = ()) -> None:
        self._values[label_values] = self._values.get(label_values, 0) + 1

    def get(self, label_values: tuple[str, ...] = ()) -> int:
        return self._values.get(label_values, 0)


@dataclass
class MetricsRegistry:
    selector_decisions_total: Counter = field(
        default_factory=lambda: Counter("selector_decisions_total", labels=("reason",))
    )
    outbox_failures_total: Counter = field(
        default_factory=lambda: Counter("outbox_failures_total", labels=("reason",))
    )


REGISTRY = MetricsRegistry()
