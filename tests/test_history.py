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



def test_two_updates_create_two_entries(client):
    res = client.post("/prompts", json={"title": "T", "body": "B"})
    pid = res.get_json()["id"]

    client.put(f"/prompts/{pid}", json={"title": "N1"})
    client.put(f"/prompts/{pid}", json={"body": "C"})

    res = client.get(f"/prompts/{pid}/history")
    history = res.get_json()
    assert len(history) == 2


def test_get_history_version(client):
    res = client.post("/prompts", json={"title": "T", "body": "B", "tags": ["a"]})
    pid = res.get_json()["id"]

    client.put(f"/prompts/{pid}", json={"title": "N1"})
    client.put(f"/prompts/{pid}", json={"body": "C"})

    res = client.get(f"/prompts/{pid}/history/0")
    entry = res.get_json()
    assert entry["title"] == "T"
    assert entry["body"] == "B"
    assert entry["tags"] == ["a"]


def test_history_version_invalid_index(client):
    res = client.post("/prompts", json={"title": "T", "body": "B"})
    pid = res.get_json()["id"]
    client.put(f"/prompts/{pid}", json={"title": "N"})

    res = client.get(f"/prompts/{pid}/history/5")
    assert res.status_code == 404


def test_history_limit_parameter(client):
    res = client.post("/prompts", json={"title": "T", "body": "B", "tags": ["a"]})
    pid = res.get_json()["id"]

    client.put(f"/prompts/{pid}", json={"title": "N1"})
    client.put(f"/prompts/{pid}", json={"body": "C"})

    res = client.get(f"/prompts/{pid}/history?limit=1")
    history = res.get_json()
    assert len(history) == 1
    entry = history[0]
    assert entry["title"] == "N1"
    assert entry["body"] == "B"
    assert entry["tags"] == ["a"]

