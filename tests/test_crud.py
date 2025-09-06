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


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_list_prompts(client):
    res = client.get("/prompts")
    assert res.status_code == 200
    assert res.get_json() == []

    client.post("/prompts", json={"title": "T1", "body": "B1"})
    client.post("/prompts", json={"title": "T2", "body": "B2"})

    res = client.get("/prompts")
    assert {p["title"] for p in res.get_json()} == {"T1", "T2"}


def test_create_and_get_prompt(client):
    res = client.post("/prompts", json={"title": "T", "body": "B"})
    assert res.status_code == 201
    pid = res.get_json()["id"]

    res = client.get(f"/prompts/{pid}")
    assert res.status_code == 200
    data = res.get_json()
    assert data["id"] == pid
    assert data["title"] == "T"
    assert data["body"] == "B"


def test_update_prompt(client):
    res = client.post("/prompts", json={"title": "T", "body": "B"})
    pid = res.get_json()["id"]

    res = client.put(f"/prompts/{pid}", json={"title": "N", "tags": ["x"]})
    assert res.status_code == 200
    data = res.get_json()
    assert data["title"] == "N"
    assert data["tags"] == ["x"}


def test_delete_prompt(client):
    res = client.post("/prompts", json={"title": "T", "body": "B"})
    pid = res.get_json()["id"]

    res = client.delete(f"/prompts/{pid}")
    assert res.status_code == 200
    assert res.get_json()["status"] == "deleted"

    res = client.get(f"/prompts/{pid}")
    assert res.status_code == 404
