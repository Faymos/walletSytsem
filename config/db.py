from pymongo import MongoClient

connection = MongoClient()
db = connection["walletsystem"]
customertables = db["Customer"]
customerAccount = db["CustomerAccount"]
customerTransaction = db["Transactions"]


    