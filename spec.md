# PromptVault – Spec (Kurz)

## Ziele
- Prompts lokal speichern (JSON)
- Abrufbar über REST
- Minimal: Create, List, Get, Update

## Endpunkte
- `GET /health` → `{ "status": "ok" }`
- `GET /prompts` → Liste aller Prompts
 - Optionaler Query-Parameter `tag` (kommagetrennt), um nach Tags zu filtern; leer/fehlend → alle Prompts
- `GET /prompts/<id>` → einzelner Prompt
- `GET /prompts/<id>/history` → Liste früherer Versionen; optional `?limit=n` → letzte n Einträge
- `GET /prompts/<id>/history/<version>` → einzelne Version nach Index (0 = älteste, -1 = neueste)
- `POST /prompts` → `{ title, body, tags?[] }` → erstellt, gibt `id` zurück
- `PUT /prompts/<id>` → ersetzt Felder
- `DELETE /prompts/<id>` → löscht einen Prompt

## Datenformat
```json
{
  "id": "pv_0001",
  "title": "Bugfix-Plan",
  "body": "Lies README, erstelle Plan, implementiere Schritt 1...",
  "tags": ["dev","plan"],
  "created_at": "2025-09-06T06:00:00Z",
  "updated_at": "2025-09-06T06:00:00Z",
  "history": [
    {
      "title": "Bugfix-Plan",
      "body": "Lies README, erstelle Plan, implementiere Schritt 1...",
      "tags": ["dev","plan"],
      "updated_at": "2025-09-06T05:00:00Z"
    }
  ]
}
```
