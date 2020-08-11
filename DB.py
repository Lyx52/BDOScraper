import json, time

from pymongo import MongoClient

from Config import Database


def make_data_model(data):

    return {
        "updated": time.time(),  # The update time
        "data": json.loads(json.dumps(data, default=lambda x: x.get_dict()))  # Dump/load data to json
    }


def connect():
    client = MongoClient(
        Database.IP,  # The Mongo server ip, pulled from config
        username=Database.User,  # The Mongo user, also from config
        password=Database.Password,  # The Auth password
        authSource=Database.DBName,  # The database used for auth
        authMechanism='SCRAM-SHA-256'  # The auth mechanism, should possibly make it configurable
    )
    database = client[Database.DBName]  # Gets the database, in which to write from the config file
    return database  # Returns database to caller function


# Drop collection
def drop(database, collection):
    database.drop_collection(collection)


def getField(database, collection, field_name):
    collection = database[collection]

    # TODO: Weird way of getting fields probably easier way...
    for item in collection.find():
        return item[field_name]


# Export the data to a mongodb collection
def export(database, data, collection):
    collection = database[collection]  # Gets the current collection from the DB
    collection.insert_one(data)
    print("Exported data to DB")
