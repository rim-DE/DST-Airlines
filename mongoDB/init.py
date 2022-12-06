from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

#host = "localhost"
host = "my_mongo"
port = 27017
user = 'admin'
password = 'pass'

myclient = MongoClient(host=host, port=port, username=user, password=password)

dblist = myclient.list_database_names()

if "aircraft" not in dblist:
    mydb = myclient['aircraft']
    mycol = mydb["positions"]
    mycol.insert_one({})
elif "aircraft" in dblist:
    mydb = myclient['aircraft']
    collist = mydb.list_collection_names()
    if "positions" not in collist:
        mycol = mydb["positions"]
        mycol.insert_one({})
"""

try:
    myclient.admin.command('ping')
    print("Connected!")
except ConnectionFailure:
        print("Server not available")
"""