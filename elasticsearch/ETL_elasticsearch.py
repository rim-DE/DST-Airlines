from extract_flight_data import FlightData
from load_flight_data_in_elasticsearch import LoadFlightData


#hosts = os.environ['ELASTICSEARCH_HOSTS']
hosts = "http://elastic-search:9200"

#Etraction des vols
user_name='rim-DE'
password='bde_airlines'
e = FlightData (user_name, password)
dict_flights=e.extractFlightData ()

l=LoadFlightData (hosts)
#connect to elasticsearch
es=l.connect()
#Chargement des vols dans elasticsearch
l.load(es, dict_flights)