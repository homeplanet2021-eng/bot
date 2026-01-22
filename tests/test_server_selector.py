import threading
from datetime import datetime

from bot.models import Server, Slot
from bot.server_selector import NoCapacityError, ServerSelector, SlotPinnedError


def _sample_servers():
    return [
        Server(
            id="nl-1",
            remnawave_node_id="node-nl",
            country_code="NL",
            city="Amsterdam",
            public_host="nl1.example.net",
            weight=10,
            max_active_slots=2,
            supported_platforms=["ios", "android"],
        ),
        Server(
            id="de-1",
            remnawave_node_id="node-de",
            country_code="DE",
            city="Frankfurt",
            public_host="de1.example.net",
            weight=5,
            max_active_slots=2,
            supported_platforms=["ios", "android"],
        ),
    ]


def test_sticky_slot_prefers_pinned():
    servers = _sample_servers()
    selector = ServerSelector(servers)
    slot = Slot(
        pinned_server_id="nl-1",
        platform_type="ios",
        status="ACTIVE",
        issued_at=datetime.utcnow(),
    )
    result = selector.select_for_slot(
        slot,
        active_slots={"nl-1": 1, "de-1": 0},
        country_code=None,
        correlation_id="corr-1",
    )
    assert result.server.id == "nl-1"
    assert result.decision.reason == "sticky"


def test_pinned_missing_raises():
    selector = ServerSelector(_sample_servers())
    slot = Slot(
        pinned_server_id="missing",
        platform_type="ios",
        status="ACTIVE",
    )
    try:
        selector.select_for_slot(slot, {}, None, "corr-2")
    except SlotPinnedError:
        assert True
    else:
        assert False, "SlotPinnedError not raised"


def test_no_capacity_raises():
    selector = ServerSelector(_sample_servers())
    slot = Slot(pinned_server_id=None, platform_type="ios", status="NEW")
    active_slots = {"nl-1": 2, "de-1": 2}
    try:
        selector.select_for_slot(slot, active_slots, None, "corr-3")
    except NoCapacityError:
        assert True
    else:
        assert False, "NoCapacityError not raised"


def test_parallel_allocation_respects_capacity():
    servers = _sample_servers()
    selector = ServerSelector(servers)
    active_slots = {"nl-1": 0, "de-1": 0}
    lock = threading.Lock()
    results = []

    def allocate():
        slot = Slot(pinned_server_id=None, platform_type="ios", status="NEW")
        with lock:
            try:
                result = selector.select_for_slot(slot, active_slots, None, "corr-4")
            except NoCapacityError:
                results.append("reject")
                return
            active_slots[result.server.id] += 1
            results.append(result.server.id)

    threads = [threading.Thread(target=allocate) for _ in range(6)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert results.count("nl-1") + results.count("de-1") <= 4
