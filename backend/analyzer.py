"""Conservative, explainable baseline menu analyzer.

This is intentionally NOT an allergy-safety classifier. An absent ingredient
is not proof that a dish is free of that ingredient.
"""
import re
from dataclasses import asdict, dataclass

EXCLUDED = {
    "egg": ["egg", "eggs", "mayonnaise", "mayo", "aioli", "hollandaise"],
    "meat_or_fish": ["chicken", "beef", "pork", "bacon", "ham", "lamb", "fish", "salmon", "tuna", "shrimp", "prawn", "anchovy", "oyster sauce", "fish sauce", "gelatin"],
}
AMBIGUOUS = ["brioche", "pasta", "noodles", "dressing", "sauce", "batter", "bun", "bread", "cake", "pastry", "fried rice", "curry", "broth"]

@dataclass
class Result:
    dish: str
    status: str
    reason: str
    evidence: str


def _mentions(text: str, term: str) -> bool:
    return bool(re.search(r"(?<!\w)" + re.escape(term) + r"(?!\w)", text, re.I))


def analyze_menu(menu_text: str) -> list[dict]:
    """Parse one dish per line: 'Dish Name - description'.

    Output is preliminary. Only explicit exclusions are classified as excluded;
    other items require confirmation until authoritative ingredient data exists.
    """
    results = []
    for line in menu_text.splitlines():
        line = line.strip().lstrip("•*- ").strip()
        if not line:
            continue
        dish, sep, description = line.partition(" - ")
        combined = f"{dish} {description}".lower()
        matches = [(category, term) for category, terms in EXCLUDED.items() for term in terms if _mentions(combined, term)]
        if matches:
            category, term = matches[0]
            result = Result(dish, "excluded", f"Menu text explicitly mentions '{term}' ({category}).", line)
        else:
            flags = [term for term in AMBIGUOUS if _mentions(combined, term)]
            note = f"Potentially hidden ingredients in: {', '.join(flags)}. " if flags else ""
            result = Result(dish, "needs_confirmation", note + "Menu descriptions alone cannot verify vegetarian and egg-free ingredients.", line)
        results.append(asdict(result))
    return results
