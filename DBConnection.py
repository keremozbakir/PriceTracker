
from pymongo import MongoClient

# connection to cluster
cluster = MongoClient(
    "mongodb+srv://kerem4022:kerem4022@playground.01kaf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = cluster["priceTracker"]
collection = db["priceTracker"]


def cluster_string():
    return cluster


def db_name():
    return db

def collection_name():
    return collection