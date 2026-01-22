"""Server selection logic with sticky slots and capacity checks."""

from __future__ import annotations

import logging
import random
from dataclasses import dataclass
from typing import Mapping, Sequence

from .models import NoCapacityError, SelectionDecision, Server, Slot, SlotPinnedError

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SelectionResult:
    server: Server
    decision: SelectionDecision


class ServerSelector:
    def __init__(self, servers: Sequence[Server]) -> None:
        self._servers = list(servers)

    def select_for_slot(
        self,
        slot: Slot,
        active_slots: Mapping[str, int],
        country_code: str | None,
        correlation_id: str,
        allow_auto: bool = True,
    ) -> SelectionResult:
        if slot.pinned_server_id:
            pinned = self._find_server(slot.pinned_server_id)
            if pinned is None:
                raise SlotPinnedError("Pinned server not found in pool.")
            if self._is_healthy_for_use(pinned, slot.platform_type, active_slots, allow_new=False):
                decision = SelectionDecision(
                    server_id=pinned.id,
                    reason="sticky",
                    correlation_id=correlation_id,
                    considered_servers=(pinned.id,),
                )
                return SelectionResult(server=pinned, decision=decision)
        return self.select_new(
            platform_type=slot.platform_type,
            active_slots=active_slots,
            country_code=country_code,
            correlation_id=correlation_id,
            allow_auto=allow_auto,
        )

    def select_new(
        self,
        platform_type: str,
        active_slots: Mapping[str, int],
        country_code: str | None,
        correlation_id: str,
        allow_auto: bool = True,
    ) -> SelectionResult:
        pool = self._filter_pool(platform_type, active_slots, country_code, allow_auto)
        if not pool:
            decision = SelectionDecision(
                server_id=None,
                reason="no_capacity",
                correlation_id=correlation_id,
                considered_servers=(),
            )
            logger.warning("No capacity for selection", extra={"decision": decision})
            raise NoCapacityError("No servers satisfy selection filters.")
        chosen = self._rank_and_pick(pool, active_slots)
        decision = SelectionDecision(
            server_id=chosen.id,
            reason="selected",
            correlation_id=correlation_id,
            considered_servers=tuple(server.id for server in pool),
        )
        logger.info("Server selected", extra={"decision": decision})
        return SelectionResult(server=chosen, decision=decision)

    def _filter_pool(
        self,
        platform_type: str,
        active_slots: Mapping[str, int],
        country_code: str | None,
        allow_auto: bool,
    ) -> list[Server]:
        pool = []
        for server in self._servers:
            if country_code and server.country_code != country_code:
                continue
            if not self._is_healthy_for_use(server, platform_type, active_slots, allow_new=True):
                continue
            pool.append(server)
        if not pool and not country_code and allow_auto:
            return []
        return pool

    @staticmethod
    def _is_healthy_for_use(
        server: Server,
        platform_type: str,
        active_slots: Mapping[str, int],
        allow_new: bool,
    ) -> bool:
        if not server.enabled:
            return False
        if server.health_status != "healthy":
            return False
        if server.maintenance_mode:
            return False
        if allow_new and server.drain_mode:
            return False
        if platform_type not in server.supported_platforms:
            return False
        return active_slots.get(server.id, 0) < server.max_active_slots

    @staticmethod
    def _rank_and_pick(pool: Sequence[Server], active_slots: Mapping[str, int]) -> Server:
        def score(server: Server) -> float:
            utilization = active_slots.get(server.id, 0) / max(server.max_active_slots, 1)
            jitter = random.random() * 0.01
            return utilization - (server.weight * 0.001) + jitter

        return min(pool, key=score)

    def _find_server(self, server_id: str) -> Server | None:
        for server in self._servers:
            if server.id == server_id:
                return server
        return None
