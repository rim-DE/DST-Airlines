from extract_flight_data import FlightData
from load_flight_data_in_elasticsearch import LoadFlightData
import os


hosts = os.environ['ELASTICSEARCH_HOSTS']
#hosts = "http://localhost:9200"

#Etraction des vols
user_name='rim-DE'
password='bde_airlines'
e = FlightData (user_name, password)
dict_flights=e.extractFliaghtData ()

l=LoadFlightData (hosts)
#connect to elasticsearch
es=l.connect()
#Chargement des vols dans elasticsearch
l.load(es, dict_flights)