from DB import drop, export, make_data_model, getField
from Config import Database, CostCalculator
from Scraper import scrapePrices, scrapeRecipes
from DB import getField
import time


def convertTime(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)


def getData(db, collectionName, isPrices=False):
    lastUpdateTime = time.time() - getField(db, collectionName, 'updated')

    print(
        f"{'Price' * isPrices + 'Recipe' * (not isPrices)} Database was last updated {convertTime(lastUpdateTime)}")
    if lastUpdateTime > Database.UpdateTime:

        # Scrape prices or recipes
        if isPrices:
            jsonObject = scrapePrices()
        else:
            jsonObject = scrapeRecipes()

        # Drop the old collection
        drop(db, collectionName)

        # Export recipes
        export(db, make_data_model(jsonObject), collectionName)

        return jsonObject

    else:
        return getField(db, collectionName, 'data')


def getRecipePrice(item_name, recipes, prices):

    recipe = recipes[item_name]
    itemCost = 0
    isFullPrice = True
    try:
        itemCost = prices[item_name]["minPrice"]
    except KeyError:
        print(f"Item ({item_name}) not in pricelist")
        pass
    materialCost = 0
    for material in recipes[item_name]:
        # Name and amount of materials
        materialName = list(material.keys())[0]
        materialAmount = list(material.values())[0]
        materialPrice = 0
        try:
            materialPrice = prices[materialName]["minPrice"]
        except KeyError:
            # Some items dont have market price or they
            print(f"Material ({materialName}) Not in pricelist")
            isFullPrice = False

        # Add to totalCost of the recipe
        materialCost = materialCost + materialPrice * materialAmount

    return {
        "materialCost": materialCost,
        "marketPrice": itemCost,
        "marketPriceAfterTax": itemCost * (0.65 + (0.195 * CostCalculator.ValuePack) + (CostCalculator.FamilyFameBonus / 100)),
        "FullMaterialPrice": isFullPrice
    }
