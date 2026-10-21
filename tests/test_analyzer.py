from backend.analyzer import analyze_menu

def test_explicit_egg_is_excluded():
    assert analyze_menu("Vegetable fried rice - rice, vegetables, egg")[0]["status"] == "excluded"

def test_explicit_meat_is_excluded():
    assert analyze_menu("Chicken salad - chicken, lettuce")[0]["status"] == "excluded"

def test_unverified_dish_needs_confirmation():
    assert analyze_menu("Margherita pizza - tomato, mozzarella, basil")[0]["status"] == "needs_confirmation"

def test_multiple_dishes():
    assert len(analyze_menu("Salad - lettuce\nSoup - carrots")) == 2
