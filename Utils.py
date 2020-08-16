from DB import drop, export, make_data_model, getField
from Config import Database, CostCalculator
from Scraper import scrapePrices, scrapeRecipes
from DB import getField
from Categories import MaterialGroups
import time, datetime


def getData(db, collectionName, isPrices=False):
    lastUpdateTime = time.time() - getField(db, collectionName, 'updated')

    print(
        f"{'Price' * isPrices + 'Recipe' * (not isPrices)} Database was last updated {datetime.timedelta(seconds=lastUpdateTime)}")
    if lastUpdateTime > Database.UpdateTime and Database.UpdateDatabases:

        # Scrape prices or recipes
        if isPrices:
            jsonObject = scrapePrices()
        else:
            jsonObject = scrapeRecipes()

        # Only drop if jsonObject has been successfuly scraped
        if jsonObject != {}:
            # Drop the old collection
            drop(db, collectionName)

        # Export recipes
        export(db, make_data_model(jsonObject), collectionName)

        return jsonObject

    else:
        return getField(db, collectionName, 'data')


def getCheapestInGroup(materialGroup, prices):
    materialPriceList = list()
    for material in MaterialGroups[materialGroup]:
        try:
            materialPriceList.append((material, prices[material]["minPrice"]))
        except KeyError:
            print(f"Item ({material}) not in pricelist")
    materialPriceList.sort(key=lambda x: x[1])
    return materialPriceList[0]


def getItemPrice(item_name, prices):
    itemName = item_name  # This gets returned because item_name can also be in a group
    itemCost = 0
    try:
        itemCost = prices[item_name]["minPrice"]
    except KeyError:
        try:
            item = getCheapestInGroup("Blood 1", prices)
            itemCost = item[1]
            itemName = item[0]
        except KeyError:
            print(f"Group and Item ({item_name}) not in pricelist")
            return item_name, 0

    return itemName, itemCost


def getRecipePrice(item_name, recipes, prices):
    recipe = recipes[item_name]
    materialList = list()

    item = getItemPrice(item_name, prices)
    itemCost = item[1]

    materialCost = 0
    for material in recipes[item_name]:
        materialTuple = getItemPrice(min(material.keys()), prices)
        # Assign values to individual variables
        materialName = materialTuple[0]
        materialPrice = materialTuple[1]
        materialAmount = min(material.values())

        # Add to totalCost of the recipe
        materialCost = materialCost + materialPrice * materialAmount
        materialList.append(material)
    return {
        "materialCost": materialCost,
        "marketPrice": itemCost,
        "marketPriceAfterTax":
            itemCost * (0.65 + (0.195 * CostCalculator.ValuePack) + (CostCalculator.FamilyFameBonus / 100)),
        "materials": materialList
    }
