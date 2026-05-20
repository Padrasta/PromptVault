def test_update_adds_history_entry(client):
    res = client.post("/prompts", json={"title": "T0", "body": "B0", "tags": ["x"]})
    pid = res.get_json()["id"]

    client.put(f"/prompts/{pid}", json={"title": "T1"})

    res = client.get(f"/prompts/{pid}/history")
    hist = res.get_json()
    assert len(hist) == 1
    entry = hist[0]
    assert entry["title"] == "T0"
    assert entry["body"] == "B0"
    assert entry["tags"] == ["x"]
    assert "updated_at" in entry


def test_history_returns_versions(client):
    res = client.post("/prompts", json={"title": "T0", "body": "B0"})
    pid = res.get_json()["id"]

    client.put(f"/prompts/{pid}", json={"title": "T1"})
    client.put(f"/prompts/{pid}", json={"title": "T2"})

    res = client.get(f"/prompts/{pid}/history")
    titles = [h["title"] for h in res.get_json()]
    assert titles == ["T0", "T1"]
