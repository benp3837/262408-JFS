import pandas as pd

# Dictionary that stores the meals the user has eaten
# KEY VALUE PAIRS! String keys and lists for items
eaten_foods = {
    "appetizers":[],
    "entrees":[],
    "desserts":[]
}

# Calculate/store the bill in a number
bill = 0

# Function to get the User's fav foods and return the menu
def generate_menu():

    appetizer = input("Name your favorite snack: ")
    eaten_foods["appetizers"].append(appetizer)

    entree = input("Name your favorite protein: ")
    eaten_foods["entrees"].append(entree)

    dessert = input("Name your favorite sweet treat: ")
    eaten_foods["desserts"].append(dessert)

    # raise a custom exception if the user says "hot dog"
    if "hot dog" in [appetizer.lower(), entree.lower(), dessert.lower()]:
        raise HotDogException()

    print("Here's your meal!")
    menu = f"""
        <~~~~~~~~~~~~~~~o~~~~~~~~~~~~~~~~>
        Your Appetizer: {appetizer} Bisque
        Your Entree: Roast {entree}
        Your Dessert: {dessert} Tart 
        <~~~~~~~~~~~~~~~o~~~~~~~~~~~~~~~~>
    """

    return menu

# Function to generate a bill based on the meals eaten
def generate_bill():

    # First, we need to make the bill variable global so we can modify it
    global bill

    # Every app is $10, every entree is $15, every dessert is $5
    # Storing these in an object for easy reference
    prices = {
        "appetizers": 10,
        "entrees": 15,
        "desserts": 5
    }

    # loop through the dictionary
    # and add to the bill based on the length of each list
    for category, items in eaten_foods.items():
        bill += len(items) * prices[category]

    # Generate and output a txt file of the bill
    with open("bill.txt", "w") as file:
        file.write("Your Bill:\n")
        file.write("====================\n")
        for category, items in eaten_foods.items():
            file.write(f"{category.capitalize()}: {len(items)} items\n")
        file.write("====================\n")
        file.write(f"Total: ${bill}\n")

    # Return the bill!
    return bill


# A function to calculate some metrics on "current" market prices
def market_analysis():

    # Hardcoded market prices
    prices = {
        "Bluefin Tuna": 42.50,
        "Yellowtail":   28.00,
        "Salmon":       18.75,
        "Uni":          65.00,
        "Hamachi":      31.00,
        "Snapper":      22.50,
        "Mackerel":     14.00,
        "Scallop":      35.00,
    }

    # Turning the market prices into a DataFrame.
    # This gives us super useful and easy to use data analysis methods from Pandas
    df = pd.DataFrame(list(prices.items()), columns=["Fish", "Price"])

    print(df.to_string(index=False))
    print()
    print(f"Average:    ${df['Price'].mean():.2f}")
    print(f"Median:     ${df['Price'].median():.2f}")
    print(f"Std Dev:    ${df['Price'].std():.2f}")
    print()
    print("Most expensive:")
    print(df.loc[df['Price'].idxmax()])
    print()
    print("Under $25:")
    print(df[df['Price'] < 25].to_string(index=False))


# Custom Exception -------------

# Custom exception inherits from Exception
class HotDogException(Exception):

    # This is the constructor, created with a "dunder" method AKA "double-underscore method"
    def __init__(self, message="Hot dogs are an unserious food"):
        self.message = message
        super().__init__(self.message) # call the super constructor