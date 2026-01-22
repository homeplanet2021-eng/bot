from datetime import datetime, timedelta

from bot.outbox import OutboxEvent, OutboxWorker


def test_outbox_process_success():
    processed = []

    def handler(event: OutboxEvent) -> None:
        processed.append(event.id)

    worker = OutboxWorker(handlers={"issue": handler})
    event = OutboxEvent(id="1", event_type="issue", payload={}, correlation_id="corr")
    updated, dlq = worker.process(event)
    assert dlq is None
    assert updated.status == "processed"
    assert processed == ["1"]


def test_outbox_retry_then_fail():
    def handler(event: OutboxEvent) -> None:
        raise RuntimeError("boom")

    worker = OutboxWorker(handlers={"issue": handler}, max_attempts=2, base_backoff_seconds=1)
    event = OutboxEvent(id="2", event_type="issue", payload={}, correlation_id="corr")
    updated, dlq = worker.process(event)
    assert dlq is None
    assert updated.status == "retrying"
    updated.next_attempt_at = datetime.utcnow() - timedelta(seconds=1)
    updated, dlq = worker.process(updated)
    assert dlq is not None
    assert updated.status == "failed"


def test_outbox_missing_handler():
    worker = OutboxWorker(handlers={})
    event = OutboxEvent(id="3", event_type="unknown", payload={}, correlation_id="corr")
    updated, dlq = worker.process(event)
    assert dlq is not None
    assert updated.status == "failed"
