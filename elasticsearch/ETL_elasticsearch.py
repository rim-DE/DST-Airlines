from extract_flight_data import FlightData
from load_flight_data_in_elasticsearch import LoadFlightData

#import sys 
#sys.path.append('../mongoDB')
#from extract_aircraft_position_data  import PositionAircraftData


#hosts = os.environ['ELASTICSEARCH_HOSTS']
#hosts = "http://localhost:9200"
hosts = "http://elastic-search:9200"

#Etraction des vols
user_name_opensky='rim-DE'
password_opensky='bde_airlines'
e = FlightData (user_name_opensky, password_opensky)
dict_flights=e.extractFlightData ()

#Etraction des positions des avions
#p = PositionAircraftData (user_name_opensky, password_opensky)
#list_dict_positions=p.extractPositionAircrafttData ()

l=LoadFlightData (hosts)
#connect to elasticsearch
es=l.connect()
#Chargement des vols dans elasticsearch
l.load(es, dict_flights)
#Chargement des positions des avions dans elasticsearch
#l.load_positions (es, list_dict_positions)