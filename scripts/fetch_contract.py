"""Fetch Remnawave contract documentation snapshot (manual stub).

This script is intentionally a stub. Operators should populate the contract file
from official Remnawave sources and update the stored hash in tests.
"""

from __future__ import annotations

from pathlib import Path

CONTRACT_PATH = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "contracts"
    / "remnawave_2.5.7_contract.md"
)


def main() -> int:
    print("fetch_contract: TODO - populate", CONTRACT_PATH)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
