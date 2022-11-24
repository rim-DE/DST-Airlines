from elasticsearch import Elasticsearch, helpers, RequestError
import time

class LoadFlightData :

    def __init__ (self, hosts):
        self.hosts = hosts
    
    def connect (self):
    
        while True:
            es = Elasticsearch(hosts = self.hosts)
            if es.ping():
                if (es.cluster.health()['status'] in ['yellow','green']):
                    break
            time.sleep(5)
        return es

    def load(self, es, dict):

        mappings = {
        "properties":{
         "icao24":{"type":"text"},
         "firstSeen":{"type":"date",
            "format": "yyyy-MM-dd HH:mm:ss"
         },
         "estDepartureAirport":{"type":"text"},
         "lastSeen":{"type":"date",
            "format": "yyyy-MM-dd HH:mm:ss"},
         "estArrivalAirport":{"type":"text"},
         "callsign":{"type":"text"},
         "estDepartureAirportHorizDistance":{"type":"text"},
         "estDepartureAirportVertDistance":{"type":"text"},
         "estArrivalAirportHorizDistance":{"type":"text"},
         "estArrivalAirportVertDistance":{"type":"text"},
         "departureAirportCandidatesCount":{"type":"text"},
         "arrivalAirportCandidatesCount":{"type":"text"}

            }
            }

        try:
            es.indices.create(index='flights', mappings=mappings)
        except RequestError as es1:
            print("L'index flights  existe déjà")
  
        print ("debut de chargement des données dans elasticsearch") 
        for doc in dict['flight']:
            es.index(index="flights", document=doc)
        print ("fin de chargement des données dans elasticsearch")
        