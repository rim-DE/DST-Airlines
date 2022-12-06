from extract_aircraft_position_data import PositionAircraftData
from load_aircraft_position_data_in_mongodb import LoadPositionAircraftData
import os 
import pprint

#user = os.environ['MONGO_INITDB_ROOT_USERNAME']
#password = os.environ['MONGO_INITDB_ROOT_PASSWORD']

host = "localhost"
#host = "my_mongo"
port = 27017
user = 'admin'
password = 'pass'

#Etraction des positions des avions
user_name_opensky='rim-DE'
password_opensky='bde_airlines'
p = PositionAircraftData (user_name_opensky, password_opensky)
dict_positions=p.extractPositionAircrafttData ('positions.json')

l=LoadPositionAircraftData (host, port, user, password)
#connect to mongodb
cl=l.connect()
#Chargement des positions dans mongodb
l.load(cl, 'positions.json')