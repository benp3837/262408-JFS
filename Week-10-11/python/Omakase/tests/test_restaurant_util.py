import pytest

from app import restaurant_util as ru

""" This test file uses pytest to test the functions in restaurant_util.py.
1) A test to check that generate_menu collects user preferences correctly.
2) A test to check that generate_menu raises a HotDogException when "hot dog" is entered.
3) A test to check that generate_bill writes the correct total to a file and returns the correct total.
4) A test to check that market_analysis prints the correct summary of market prices.
"""

# A fixture is a function that runs before each test to set up the environment.
# In this case, it resets the state of the eaten_foods and bill variables before each test runs.
@pytest.fixture(autouse=True)
def reset_state():
    ru.eaten_foods["appetizers"].clear()
    ru.eaten_foods["entrees"].clear()
    ru.eaten_foods["desserts"].clear()
    ru.bill = 0

# These tests use the "monkeypatch" fixture to simulate user input in the functions

def test_generate_menu_collects_preferences(monkeypatch):

    responses = ["fries", "salmon", "cake"]

    monkeypatch.setattr("builtins.input", lambda _prompt="": responses.pop(0))

    menu = ru.generate_menu()

    assert ru.eaten_foods == {
        "appetizers": ["fries"],
        "entrees": ["salmon"],
        "desserts": ["cake"],
    }
    assert "Your Appetizer: fries Bisque" in menu
    assert "Your Entree: Roast salmon" in menu
    assert "Your Dessert: cake Tart" in menu


def test_generate_menu_raises_for_hot_dog(monkeypatch):

    responses = ["hot dog", "salmon", "cake"]
    monkeypatch.setattr("builtins.input", lambda _prompt="": responses.pop(0))

    with pytest.raises(ru.HotDogException, match="Hot dogs are an unserious food"):
        ru.generate_menu()

# This one uses the "tmp_path" fixture to create a temporary directory for the bill file,
# and checks that the bill is written correctly and the total is returned correctly.

def test_generate_bill_writes_and_returns_total(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    ru.eaten_foods["appetizers"] = ["soup", "salad"]
    ru.eaten_foods["entrees"] = ["salmon", "beef"]
    ru.eaten_foods["desserts"] = ["cake"]

    total = ru.generate_bill()

    assert total == 10 * 2 + 15 * 2 + 5 * 1
    assert (tmp_path / "bill.txt").read_text() == (
        "Your Bill:\n"
        "====================\n"
        "Appetizers: 2 items\n"
        "Entrees: 2 items\n"
        "Desserts: 1 items\n"
        "====================\n"
        "Total: $55\n"
    )

# Finally, this test uses the "capsys" fixture
# to capture the output of the market_analysis function

def test_market_analysis_prints_summary(capsys):
    ru.market_analysis()

    captured = capsys.readouterr().out
    assert "Average:" in captured
    assert "$32.09" in captured
    assert "Median:" in captured
    assert "$29.50" in captured
    assert "Most expensive:" in captured
    assert "Uni" in captured
    assert "Under $25:" in captured
    assert "Salmon" in captured
    assert "Mackerel" in captured
