from elasticsearch import Elasticsearch, helpers, RequestError
import json
import sys

es = Elasticsearch(hosts = "http://172.29.213.152:9200")


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
  print('Index already exists')
  

with open('flights_data.json', encoding='utf-8') as f:
    data = json.load(f)
    for doc in data['flight']:
        es.index(index="flights", document=doc)
        