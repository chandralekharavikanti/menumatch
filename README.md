# MenuMatch

**Search any restaurant. Find dishes that match your diet — with evidence when available.**

MenuMatch is being built as an on-demand restaurant menu discovery and dietary analysis app. The initial dietary profile is vegetarian **without eggs**, with dairy allowed.

## Current milestone: local menu-text screening

This starter implements a working FastAPI service and conservative, deterministic baseline analyzer. It detects explicitly mentioned meat, fish, or egg ingredients. **All other dishes are marked `needs_confirmation`** until ingredient and allergen evidence can be retrieved. It does not claim food is allergy-safe.

### Setup in VS Code (macOS/Linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
python -m uvicorn backend.main:app --reload
```

On Windows PowerShell, activate with `.venv\\Scripts\\Activate.ps1` instead.

Open http://127.0.0.1:8000/docs to try the interactive API. Use **POST /analyze** with:

```json
{
  "menu_text": "Vegetable fried rice - rice, carrots, egg\nMargherita pizza - tomato, mozzarella, basil"
}
```

### Roadmap

1. Menu ingestion from HTML, PDF, and user-provided images.
2. On-demand restaurant identification and official website discovery.
3. Evidence retrieval from official ingredient and allergen sources.
4. Source-grounded classification and uncertainty handling.
5. React frontend, caching, evaluations, deployment.

**Important:** The current API is a starting baseline, not a production dietary recommendation engine. No live restaurant search, RAG, LLM, or agent has been implemented yet.
