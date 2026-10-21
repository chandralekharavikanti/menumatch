"""MenuMatch API — first local milestone."""
from fastapi import FastAPI
from pydantic import BaseModel, Field
from backend.analyzer import analyze_menu

app = FastAPI(title="MenuMatch API", version="0.1.0")

class MenuRequest(BaseModel):
    menu_text: str = Field(min_length=1, description="One dish per line: Dish - description")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze")
def analyze(request: MenuRequest):
    return {"results": analyze_menu(request.menu_text), "disclaimer": "Preliminary menu-text screening only; not proof of allergen safety. Verify with the restaurant."}
