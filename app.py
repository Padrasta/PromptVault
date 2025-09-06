
# app.py (minimal, läuft sofort)

from flask import Flask, jsonify, request
from pathlib import Path
import json, os, time

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
    return jsonify(load_data())

@app.get("/prompts/<pid>")
def get_prompt(pid):
    items = load_data()
    for it in items:
        if it["id"] == pid:
            return jsonify(it)
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
            it["title"] = body.get("title", it["title"])
            it["body"]  = body.get("body", it["body"])
            it["tags"]  = body.get("tags", it["tags"])
            it["updated_at"] = now_iso()
            save_data(items)
            return jsonify(it)
    return jsonify({"error": "not found"}), 404

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="127.0.0.1", port=port, debug=True)
