from pathlib import Path

import pytest

CONTRACT_PATH = (
    Path(__file__).resolve().parents[2]
    / "docs"
    / "contracts"
    / "remnawave_2.5.7_contract.md"
)


def _is_verified(contract_text: str) -> bool:
    for line in contract_text.splitlines():
        if line.strip().startswith("- verified:"):
            return line.strip().endswith("true")
    return False


def test_contract_is_verified_or_xfail():
    contract_text = CONTRACT_PATH.read_text(encoding="utf-8")
    if not _is_verified(contract_text):
        pytest.xfail("Contract not verified; SAFE MODE required.")
    assert "Endpoints" in contract_text
    assert "Models" in contract_text
    assert "Errors" in contract_text
