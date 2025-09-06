# PromptVault – Minimal lauffähiges Skelett

Ein schlankes Repository, mit dem Codex & VS Code sofort arbeiten können:
- klarer Entrypoint (`app.py`)
- einheitliche Startbefehle
- Mini-Test & Beispieldaten
- kurze Spezifikation (spec.md)

## 1) Quickstart (Windows)

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Umgebungsvariablen laden (manuell aus .env.example kopieren)
set FLASK_APP=app.py
set FLASK_ENV=development
set PORT=8000

# Start
flask run -p %PORT%
# PromptVault
