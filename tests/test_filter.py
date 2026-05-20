from typing import List


def seed_prompts(client) -> List[str]:
    ids = []
    res = client.post("/prompts", json={"title": "T1", "body": "B1", "tags": ["demo"]})
    ids.append(res.get_json()["id"])
    res = client.post("/prompts", json={"title": "T2", "body": "B2", "tags": ["plan"]})
    ids.append(res.get_json()["id"])
    res = client.post("/prompts", json={"title": "T3", "body": "B3", "tags": ["demo", "plan"]})
    ids.append(res.get_json()["id"])
    return ids


def test_no_tag_returns_all(client):
    seed_prompts(client)
    res = client.get("/prompts")
    assert {p["title"] for p in res.get_json()} == {"T1", "T2", "T3"}


def test_empty_tag_returns_all(client):
    seed_prompts(client)
    res = client.get("/prompts?tag=")
    assert {p["title"] for p in res.get_json()} == {"T1", "T2", "T3"}


def test_single_tag_filter(client):
    seed_prompts(client)
    res = client.get("/prompts?tag=demo")
    assert {p["title"] for p in res.get_json()} == {"T1", "T3"}


def test_multi_tag_filter(client):
    seed_prompts(client)
    res = client.get("/prompts?tag=demo,plan")
    assert {p["title"] for p in res.get_json()} == {"T1", "T2", "T3"}


def test_unknown_tag(client):
    seed_prompts(client)
    res = client.get("/prompts?tag=unknown")
    assert res.get_json() == []
