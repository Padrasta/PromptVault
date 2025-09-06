
# app.py (minimal, läuft sofort)

from flask import Flask, jsonify, request
from pathlib import Path
import json
import os
import time

app = Flask(__name__)
DATA_PATH = Path("prompts/sample.json")
DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
if not DATA_PATH.exists():
    DATA_PATH.write_text(json.dumps([], indent=2), encoding="utf-8")

def now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def load_data():
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))

def save_data(items):
    DATA_PATH.write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.get("/prompts")
def list_prompts():
    items = load_data()
    tag_param = request.args.get("tag", "").strip()
    if tag_param:
        tags = {t.strip() for t in tag_param.split(",") if t.strip()}
        if tags:
            items = [p for p in items if any(t in p.get("tags", []) for t in tags)]
    return jsonify(items)

@app.get("/prompts/<pid>")
def get_prompt(pid):
    items = load_data()
    for it in items:
        if it["id"] == pid:
            return jsonify(it)
    return jsonify({"error": "not found"}), 404


@app.get("/prompts/<pid>/history")
def get_history(pid):
    items = load_data()
    for it in items:
        if it["id"] == pid:
            return jsonify(it.get("history", []))
    return jsonify({"error": "not found"}), 404

@app.post("/prompts")
def create_prompt():
    body = request.get_json(force=True, silent=True) or {}
    title = (body.get("title") or "").strip()
    text  = (body.get("body") or "").strip()
    tags  = body.get("tags") or []
    if not title or not text:
        return jsonify({"error": "title and body required"}), 400
    items = load_data()
    new_id = f"pv_{len(items)+1:04d}"
    item = {
        "id": new_id,
        "title": title,
        "body": text,
        "tags": tags,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "history": [],
    }
    items.append(item)
    save_data(items)
    return jsonify(item), 201

@app.put("/prompts/<pid>")
def update_prompt(pid):
    body = request.get_json(force=True, silent=True) or {}
    items = load_data()
    for it in items:
        if it["id"] == pid:
            prev = {
                "title": it["title"],
                "body": it["body"],
                "updated_at": it.get("updated_at") or now_iso(),
            }
            if "tags" in it:
                prev["tags"] = list(it.get("tags", []))
            it.setdefault("history", []).append(prev)

            it["title"] = body.get("title", it["title"])
            it["body"] = body.get("body", it["body"])
            it["tags"] = body.get("tags", it.get("tags"))
            it["updated_at"] = now_iso()
            save_data(items)
            return jsonify(it)
    return jsonify({"error": "not found"}), 404


@app.delete("/prompts/<pid>")
def delete_prompt(pid):
    items = load_data()
    for idx, it in enumerate(items):
        if it["id"] == pid:
            items.pop(idx)
            save_data(items)
            return jsonify({"status": "deleted"})
    return jsonify({"error": "not found"}), 404

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="127.0.0.1", port=port, debug=True)
