import pytest


def test_update_creates_history_entry(client):
    res = client.post("/prompts", json={"title": "T", "body": "B", "tags": ["x"]})
    pid = res.get_json()["id"]

    res = client.get(f"/prompts/{pid}/history")
    assert res.status_code == 200
    assert res.get_json() == []

    res = client.put(f"/prompts/{pid}", json={"title": "N"})
    assert res.status_code == 200

    res = client.get(f"/prompts/{pid}/history")
    history = res.get_json()
    assert len(history) == 1
    entry = history[0]
    assert entry["title"] == "T"
    assert entry["body"] == "B"
    assert entry["tags"] == ["x"]
    assert "updated_at" in entry


def test_history_returns_versions(client):
    res = client.post("/prompts", json={"title": "T", "body": "B", "tags": ["a"]})
    pid = res.get_json()["id"]

    client.put(f"/prompts/{pid}", json={"title": "N"})
    client.put(f"/prompts/{pid}", json={"body": "C", "tags": ["b"]})

    res = client.get(f"/prompts/{pid}/history")
    history = res.get_json()
    assert len(history) == 2
    assert history[0]["title"] == "T"
    assert history[0]["body"] == "B"
    assert history[0]["tags"] == ["a"]
    assert history[1]["title"] == "N"
    assert history[1]["body"] == "B"
    assert history[1]["tags"] == ["a"]
