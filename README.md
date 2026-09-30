# PocketSmart AI

Complete FastAPI + Jinja2 + SQLite + Gemini application based on the supplied PocketSmart AI documentation.

## Features

- Home Interior Planner
- Party Budget Planner
- Jewelry Planner with optional outfit image
- Gemini structured recommendations
- Demo mode for testing without an API key
- Registration/login/logout using JWT in an HttpOnly cookie
- SQLite recommendation history
- Responsive frontend
- Validation and error handling
- API documentation at `/docs`
- Pytest tests
- GitHub-safe `.gitignore`

## Important model note

The supplied documentation names Gemini 1.5 Flash Pro. That is an older model requirement. The model is configurable through `GEMINI_MODEL`; this build defaults to `gemini-2.5-flash`. Change it in `.env` if required.

The application does not fake live Amazon/Flipkart/IKEA/Swiggy/Zomato/OYO inventory. Gemini produces planning recommendations and the backend creates platform search links. Prices are explicitly treated as estimates.

## Windows / VS Code setup

1. Install Python 3.11+.
2. Open this folder in VS Code.
3. Open Terminal.
4. Create the environment:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

5. Install packages:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

6. Copy `.env.example` to `.env`.

For a first test without Gemini:

```env
DEMO_MODE=true
```

For real AI:

```env
DEMO_MODE=false
GEMINI_API_KEY=YOUR_KEY
GEMINI_MODEL=gemini-2.5-flash
```

7. Run:

```powershell
python run.py
```

or:

```powershell
python -m uvicorn app.main:app --reload
```

8. Open `http://127.0.0.1:8000`.

API docs: `http://127.0.0.1:8000/docs`

Health: `http://127.0.0.1:8000/health`

9. Run tests:

```powershell
pytest -q
```

## User flow

Register -> Login -> Dashboard -> choose Home/Party/Jewelry -> enter budget -> generate -> inspect platform search links -> History.

## Project tree

```text
PocketSmartAI/
├── app/
│   ├── main.py config.py database.py models.py schemas.py auth.py dependencies.py
│   ├── routers/
│   │   ├── pages.py auth.py api.py
│   └── services/
│       ├── gemini_service.py recommendation_service.py platform_links.py
├── static/css/styles.css
├── static/js/app.js
├── templates/
├── tests/
├── uploads/.gitkeep
├── .env.example
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

## GitHub

```powershell
git init
git add .
git commit -m "Build PocketSmart AI"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/PocketSmartAI.git
git push -u origin main
```

Never commit `.env`, `.venv`, databases, or uploaded images.
