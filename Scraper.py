import time, requests
from lxml import html
from Config import Scraper
from Categories import Categories, SubCategories, Links


def getItemPrice(category_id, sub_category_id):
    lastTime = time.time()
    url = Links["MarketList"]

    headers = Scraper.HeaderData

    form_data = {
        'mainCategory': category_id,
        'subCategory': sub_category_id,
        '__RequestVerificationToken': Scraper.RequestVerificationToken
    }

    req = requests.post(url, data=form_data, headers=headers)

    if req.status_code != 200:
        print("Request not fulfilled!")

    res_json = req.json()
    item_dict = {}

    for item in res_json['marketList']:
        item_dict[item['name']] = \
            {
                "id": item['mainKey'],
                "minPrice": item['minPrice']
            }
    time.sleep(Scraper.TimeBetweenRequests % (time.time() - lastTime))

    # If list is not empty
    if item_dict != {}:
        print(f"Items in Subcategory ({SubCategories[Categories[category_id]][sub_category_id]}) of Category ({Categories[category_id]}) added")
        return item_dict
    else:
        print("Price request or parsing failed!")


def scrapePrices(minCat=0, maxCat=80):
    data = list()
    for catID in Categories:
        if maxCat < catID < minCat:
            continue
        for subID in SubCategories[Categories[catID]]:
            data = data + list(getItemPrice(catID, subID).items())
    return dict(data)


def scrapeRecipes(maxID=200):
    data = {}
    for id in range(1, maxID):
        lastTime = time.time()
        recipe = getItemRecipe(id)
        data[list(recipe)[0]] = list(recipe.values())[0]
        time.sleep(Scraper.TimeBetweenRequests % (time.time() - lastTime))
        print(f"Item {list(recipe.keys())[0]} recipe added")

    return data


def getItemRecipe(recipe_id):
    url = Links["RecipeSite"]

    # TODO: Get rid of this hacky piece of code...

    # Request html with the recipe id
    x = requests.get(url=url + f"{recipe_id}/")

    # Create root object
    root = html.fromstring(x.content)

    # Get name of the craftable item
    name = root.xpath('//span[@id="item_name"]//text()')[0]

    # Get recipe material names
    materials = list(root.xpath('//tr[5]//a[@data-enchant="0"]/text()'))
    materialNames = list()
    if len(materials) > 0:
        # Removing html bs
        for item in materials:
            if '\r\n' not in item:
                materialNames.append(item)
    else:
        print("Item recipe does not exist or cannot be parsed!")
        pass

    # Get amount of each material required
    materialCount = list(root.xpath('//tr[5]//a/div[@class="quantity_small nowrap"]//text()'))
    output = list()
    for material in materialNames:
        if len(materialCount) < len(materialNames):
            # If there is no item count in the list then add 1 to required amount
            for index in range(len(materialNames) - len(materialCount)):
                materialCount.insert(index, 1)
        # Add material to output list
        output.append({
            material: int(materialCount[materialNames.index(material)])
        })
    return {
        name: output
    }
