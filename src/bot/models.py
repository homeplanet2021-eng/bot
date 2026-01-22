"""Core models for server selection and slots."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable


@dataclass(frozen=True)
class Server:
    id: str
    remnawave_node_id: str
    country_code: str
    city: str
    public_host: str
    weight: int
    max_active_slots: int
    tags: list[str] = field(default_factory=list)
    maintenance_mode: bool = False
    enabled: bool = True
    drain_mode: bool = False
    supported_platforms: list[str] = field(default_factory=list)
    health_status: str = "healthy"


@dataclass
class Slot:
    pinned_server_id: str | None
    platform_type: str
    status: str
    issued_at: datetime | None = None
    last_action_at: datetime | None = None
    transfer_count_month: int = 0
    reissue_count_day: int = 0


@dataclass(frozen=True)
class SelectionDecision:
    server_id: str | None
    reason: str
    correlation_id: str
    considered_servers: tuple[str, ...]


class NoCapacityError(RuntimeError):
    """Raised when no servers can satisfy the selection request."""


class SlotPinnedError(RuntimeError):
    """Raised when a slot is pinned to a server not in the pool."""


class ServerPool:
    """Simple in-memory server inventory."""

    def __init__(self, servers: Iterable[Server]) -> None:
        self._servers = {server.id: server for server in servers}

    def list(self) -> list[Server]:
        return list(self._servers.values())

    def get(self, server_id: str) -> Server | None:
        return self._servers.get(server_id)
