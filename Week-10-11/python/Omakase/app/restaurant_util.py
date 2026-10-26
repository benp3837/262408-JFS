# Dictionary that stores the meals the user has eaten
# KEY VALUE PAIRS! String keys and lists for values
eaten_foods = {
    "appetizers":[],
    "entrees":[],
    "desserts":[]
}

#TODO: Calculate bill in a number var

# Function to get the User's fav foods and return the menu
def generate_menu():
    appetizer = input("Name your favorite snack: ")
    eaten_foods["appetizers"].append(appetizer)

    entree = input("Name your favorite protein: ")
    eaten_foods["entrees"].append(entree)

    dessert = input("Name your favorite sweet treat: ")
    eaten_foods["desserts"].append(dessert)

    return eaten_foods


# Function to serve the user, and save meals above

