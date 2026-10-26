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

    # TODO: abstract this into a function
    appetizer = input("Name your favorite snack: ")
    entree = input("Name your favorite protein: ")
    dessert = input("Name your favorite sweet treat: ")

    # TODO: serve the user and give them a price
    print("Here is your meal! Here's your bill!")

    # Toggle the while loop boolean (or not)
    print("Are you still hungry? (yes/no)")
    still_hungry = input("> ").strip().lower()

    if still_hungry == "no":
        hungry = False
        print("Thanks for coming, see you next time!")
    else:
        print("Great, let's make you another meal!")