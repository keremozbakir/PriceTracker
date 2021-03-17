from pymongo import MongoClient


#connection to cluster
cluster=MongoClient("mongodb+srv://kerem4022:kerem4022@nodetuts.7fmw3.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db=cluster["priceTracker"]
collection=db["priceTracker"]
#inserting to database
post={"_id":0, "website":"otto", "link":"https://www.otto.de/p/call-of-duty-modern-warfare-xbox-one-904656898/#variationId=904656899",}
collection.insert_one(post)


