from pathlib import Path

import pytest

CONTRACT_PATH = (
    Path(__file__).resolve().parents[2]
    / "docs"
    / "contracts"
    / "remnawave_2.5.7_contract.md"
)
EXPECTED_SHA256 = "1f47c52d6315f4dd6eb2aba66d104bf286a1cc3fec5649029c6f63643f1ac030"


def _is_verified(contract_text: str) -> bool:
    for line in contract_text.splitlines():
        if line.strip().startswith("- verified:"):
            return line.strip().endswith("true")
    return False


def test_contract_is_verified_or_xfail():
    contract_bytes = CONTRACT_PATH.read_bytes()
    contract_text = contract_bytes.decode("utf-8")
    if not _is_verified(contract_text):
        pytest.xfail("Contract not verified; SAFE MODE required.")
    assert "Endpoints" in contract_text
    assert "Models" in contract_text
    assert "Errors" in contract_text


def test_contract_snapshot_hash():
    import hashlib

    contract_bytes = CONTRACT_PATH.read_bytes()
    digest = hashlib.sha256(contract_bytes).hexdigest()
    assert digest == EXPECTED_SHA256
