import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
import app as pv


def test_delete_prompt(tmp_path, monkeypatch):
    data_file = tmp_path / "data.json"
    monkeypatch.setattr(pv, "DATA_PATH", data_file)
    data_file.parent.mkdir(parents=True, exist_ok=True)
    data_file.write_text("[]", encoding="utf-8")
    client = pv.app.test_client()

    res = client.post("/prompts", json={"title": "T", "body": "B"})
    pid = res.get_json()["id"]

    res = client.delete(f"/prompts/{pid}")
    assert res.status_code == 200
    assert res.get_json()["status"] == "deleted"

    res = client.get(f"/prompts/{pid}")
    assert res.status_code == 404
