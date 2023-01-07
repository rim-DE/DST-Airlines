"""
from extract_flight_data import FlightData
from load_flight_data_in_elasticsearch import LoadFlightData
from update_data_in_elastic_search import UpdateDataInES
from datetime import datetime, timedelta



#hosts = os.environ['ELASTICSEARCH_HOSTS']
hosts = "http://localhost:9200"
#hosts = "http://elastic-search:9200"

#Etraction des vols
user_name_opensky='rim-DE'
password_opensky='bde_airlines'
e = FlightData (user_name_opensky, password_opensky)
e.extractFlightData ('flights_test.json')
"""

"""
l=LoadFlightData (hosts)
#connect to elasticsearch
es=l.connect()
#Chargement des vols dans elasticsearch
l.load(es, 'flights.json')
#Chargement des positions des avions dans elasticsearch
#l.load_positions (es, list_dict_positions)
"""
"""

u=UpdateDataInES (hosts)
#connect to elasticsearch
es=u.connect()

u.deleteOldData (es)"""

from extract_flight_data import FlightData
from load_flight_data_in_elasticsearch import LoadFlightData


#hosts = os.environ['ELASTICSEARCH_HOSTS']
hosts = "http://localhost:9200"

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