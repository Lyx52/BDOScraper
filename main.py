from DB import connect
from Config import Database
from Utils import getData, getRecipePrice

# Connect to database
db = connect()

recipes = getData(db, Database.RecipeCollection)
prices = getData(db, Database.PriceCollection, isPrices=True)


# Temp code
profitableRecipes = list()
for recipe in recipes['data']:
    recipeCosts = list()
    recipeCosts.append(getRecipePrice(recipe, recipes['data'], prices))
    if recipes['info'][recipe]['disabled']:
        print(f"{recipe} is disabled!")
    # Todo: Some hashmaps myb :))))
    for recipeCost in recipeCosts:
        recipeProfit = recipeCost['marketPriceAfterTax'] - recipeCost['materialCost']
        if recipeProfit > 0:
            print(f"Profitable item {recipe} with material cost {recipeCost['materialCost']} and silver profit: {recipeProfit}")
            print(f"Item materials {recipeCost['materials']} \n")
            profitableRecipes.append({recipe: recipeCost})

print(profitableRecipes)
