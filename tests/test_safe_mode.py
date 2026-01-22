from pathlib import Path

from bot.safe_mode import contract_verified, safe_mode_required


def test_safe_mode_required_when_unverified(tmp_path: Path) -> None:
    contract = tmp_path / "contract.md"
    contract.write_text("- verified: false", encoding="utf-8")
    assert contract_verified(contract) is False
    assert safe_mode_required(contract) is True


def test_safe_mode_not_required_when_verified(tmp_path: Path) -> None:
    contract = tmp_path / "contract.md"
    contract.write_text("- verified: true", encoding="utf-8")
    assert contract_verified(contract) is True
    assert safe_mode_required(contract) is False
