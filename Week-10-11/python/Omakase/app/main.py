"""
Omakase is basically where you show up to a restaurant and the chef serves whatever they want
-It's usually a couple courses based on things like occasions, seasonality, etc.

We'll be creating an Omakase-ish CLI that demonstrates:
-User input/output
-Data Structures (lists, dictionaries)
-Control Flow
-Functions
"""
from operator import truediv

from app.restaurant_util import generate_menu

print("""
                  *===========####===========*
                  Welcome to the Omakase CLI!

We'll create a curated dining experience based on your favorite foods
*================================####================================*
""")


print("First, what's your name?")
name = input(">")

print(f"Nice to meet you {name}!")

# This boolean will determine whether the app continues running
hungry = True

# While loop that depends on "Hungry"
while hungry:

    # Call generate menu to get the user's foods and show a menu
    generated_menu = generate_menu()

    print(generated_menu)

    # Give the user the bill for their meal
    print("Here's your bill!")

    # Toggle the while loop boolean (or not)
    print("Are you still hungry? (yes/no)")
    still_hungry = input("> ").strip().lower()

    if still_hungry == "no":
        hungry = False
        print("Thanks for coming, see you next time!")
    else:
        print("Great, let's make you another meal!")