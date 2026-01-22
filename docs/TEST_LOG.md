# Test Log

## 2025-09-27

| Command | Result | Notes |
| --- | --- | --- |
| `python -m venv .venv` | ✅ PASS | Virtual environment created. |
| `. .venv/bin/activate && pip install -r requirements.txt` | ⚠️ FAIL | Proxy blocked access to PyPI (HTTP 403). |
| `. .venv/bin/activate && ruff check .` | ✅ PASS | All checks passed. |
| `. .venv/bin/activate && mypy .` | ✅ PASS | No issues found. |
| `. .venv/bin/activate && pytest -q` | ✅ PASS | Test suite completed (1 xfailed). |
| `. .venv/bin/activate && alembic upgrade head` | ⚠️ FAIL | `alembic` missing due to pip install failure. |
| `. .venv/bin/activate && python scripts/simulate_flow.py` | ✅ PASS | Flow simulation completed. |
| `docker compose -f docker-compose.dev.yml up -d` | ⚠️ FAIL | Docker unavailable in environment. |

## Reference commands used for deployment guidance
- `nl -ba docs/INTEGRATION_GUIDE.md`
- `nl -ba .env.example`
- `nl -ba config/servers.yml`
- `nl -ba docs/INPUTS_REQUIRED.md`
- `sed -n '1,200p' docker-compose.prod.yml`
