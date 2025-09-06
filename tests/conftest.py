import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))
import app as pv


@pytest.fixture()
def client(tmp_path, monkeypatch):
    data_file = tmp_path / "data.json"
    data_file.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(pv, "DATA_PATH", data_file)
    return pv.app.test_client()
