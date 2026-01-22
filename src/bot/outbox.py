"""Outbox and DLQ primitives."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Protocol


@dataclass
class OutboxEvent:
    id: str
    event_type: str
    payload: dict
    correlation_id: str
    status: str = "pending"
    attempt_count: int = 0
    next_attempt_at: datetime | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class DLQEvent:
    id: str
    event_type: str
    payload: dict
    correlation_id: str
    failed_at: datetime = field(default_factory=datetime.utcnow)
    reason: str = ""


class EventHandler(Protocol):
    def __call__(self, event: OutboxEvent) -> None: ...


@dataclass
class OutboxWorker:
    handlers: dict[str, EventHandler]
    max_attempts: int = 5
    base_backoff_seconds: int = 5

    def process(self, event: OutboxEvent) -> tuple[OutboxEvent, DLQEvent | None]:
        handler = self.handlers.get(event.event_type)
        if handler is None:
            return self._fail(event, "handler_not_found")
        if event.next_attempt_at and event.next_attempt_at > datetime.utcnow():
            return event, None
        try:
            handler(event)
        except Exception as exc:  # noqa: BLE001 - capture handler failures
            return self._retry(event, str(exc))
        event.status = "processed"
        event.updated_at = datetime.utcnow()
        return event, None

    def _retry(self, event: OutboxEvent, reason: str) -> tuple[OutboxEvent, DLQEvent | None]:
        event.attempt_count += 1
        event.updated_at = datetime.utcnow()
        if event.attempt_count >= self.max_attempts:
            return self._fail(event, reason)
        delay = timedelta(seconds=self.base_backoff_seconds * event.attempt_count)
        event.next_attempt_at = datetime.utcnow() + delay
        event.status = "retrying"
        return event, None

    def _fail(self, event: OutboxEvent, reason: str) -> tuple[OutboxEvent, DLQEvent | None]:
        event.status = "failed"
        event.updated_at = datetime.utcnow()
        dlq = DLQEvent(
            id=event.id,
            event_type=event.event_type,
            payload=event.payload,
            correlation_id=event.correlation_id,
            reason=reason,
        )
        return event, dlq
