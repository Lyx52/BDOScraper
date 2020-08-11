from DB import connect
from Config import Database
from Utils import getData, getRecipePrice

# Connect to database
db = connect()

recipes = getData(db, Database.RecipeCollection)
prices = getData(db, Database.PriceCollection, isPrices=True)
for recipe in recipes:
    print(getRecipePrice(recipe, recipes, prices))

