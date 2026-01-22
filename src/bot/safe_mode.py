"""SAFE MODE guard utilities."""

from __future__ import annotations

from pathlib import Path


def contract_verified(contract_path: Path) -> bool:
    content = contract_path.read_text(encoding="utf-8")
    for line in content.splitlines():
        if line.strip().startswith("- verified:"):
            return line.strip().endswith("true")
    return False


def safe_mode_required(contract_path: Path) -> bool:
    return not contract_verified(contract_path)
