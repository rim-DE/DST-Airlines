from extract_aircraft_position_data import PositionAircraftData
from load_aircraft_position_data_in_mongodb import LoadPositionAircraftData
import os 
import pprint
from pymongo import MongoClient

#user = os.environ['MONGO_INITDB_ROOT_USERNAME']
#password = os.environ['MONGO_INITDB_ROOT_PASSWORD']

host = "localhost"
#host = "my_mongo"
port = 27017
user = 'admin'
password = 'pass'

client = MongoClient(host= host, port=port, username=user, password=password)
mydb = client['aircraft']    
cursor = mydb.positions.find({'icao24':'511142'})
for doc in cursor:
    pprint.pp(doc)
     

'''
#Etraction des positions des avions
user_name_opensky='rim-DE'
password_opensky='bde_airlines'
p = PositionAircraftData (user_name_opensky, password_opensky)
p.extractPositionAircrafttData ('positions.json')

l=LoadPositionAircraftData (host, port, user, password)
#connect to mongodb
cl=l.connect()
#Chargement des positions dans mongodb
l.load(cl, 'positions.json')
'''