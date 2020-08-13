class Database:
    IP = "localhost:27017"
    User = "User"
    Password = "Password"
    DBName = "BDODB"
    RecipeCollection = "RecipeData"
    PriceCollection = "PriceData"
    UpdateTime = 3600   # Time in seconds


class Scraper:
    TimeBetweenRequests = 0.5

    # Needs to be supplied from your own login,
    RequestVerificationToken = ""
    HeaderData = {
        'Cookie': "",
        'User-Agent': ""
    }


class CostCalculator:
    ValuePack = True
    FamilyFameBonus = 0.5   # In %
