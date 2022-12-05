from elasticsearch import Elasticsearch, helpers, RequestError
import time

class LoadFlightData :

    def __init__ (self, hosts):
        self.hosts = hosts
    
    def connect (self):
      es = Elasticsearch(hosts = self.hosts)
        
      """
        while True:
            es = Elasticsearch(hosts = self.hosts)
            if es.ping():
                if (es.cluster.health()['status'] in ['yellow','green']):
                    break
            time.sleep(5)
      """
      return es

    def load(self, es, dict):

      mappings = {
      "properties" : {
        "arrivalAirportCandidatesCount" : {
          "type" : "integer",
          "fields" : {
            "keyword" : {
              "type" : "keyword"
            }
          }
        },
        "callsign" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword"
            }
          }
        },
        "departureAirportCandidatesCount" : {
          "type" : "integer",
          "fields" : {
            "keyword" : {
              "type" : "keyword"
            }
          }
        },
        "estArrivalAirport" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword"
            }
          }
        },
        "estArrivalAirportHorizDistance" : {
          "type" : "integer",
          "fields" : {
            "keyword" : {
              "type" : "keyword"
            }
          }
        },
        "estArrivalAirportVertDistance" : {
          "type" : "integer",
          "fields" : {
            "keyword" : {
              "type" : "keyword"
            }
          }
        },
        "estDepartureAirport" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword"
            }
          }
        },
        "estDepartureAirportHorizDistance" : {
          "type" : "integer",
          "fields" : {
            "keyword" : {
              "type" : "keyword"
            }
          }
        },
        "estDepartureAirportVertDistance" : {
          "type" : "integer",
          "fields" : {
            "keyword" : {
              "type" : "keyword"
            }
          }
        },
        "firstSeen" : {
          "type" : "date",
          "format" : "yyyy-MM-dd HH:mm:ss"
        },
        "icao24" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword"
            }
          }
        },
        "lastSeen" : {
          "type" : "date",
          "format" : "yyyy-MM-dd HH:mm:ss"
        }
        }
      }

      try:
          es.indices.create(index='flights', mappings=mappings)
      except RequestError as es1:
          print("L'index flights existe déjà")
  
      print ("debut de chargement des données dans elasticsearch") 
      for doc in dict['flight']:
          es.index(index="flights", document=doc)
      print ("fin de chargement des données dans elasticsearch")
        

    def load_positions (self, es, list_dict_positions):

        mappings = {
        "properties" : {
        "icao24" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "callsign" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "origin_country" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "time_position" : {
          "type" : "text",
          
        },
        "last_contact" : {
          "type" : "text",
          
        },
        "long" : {
          "type" : "text",
        
        },
        "lat" : {
          "type" : "text",
        
        },
        "baro_altitude" : {
          "type" : "text",
        
        },
        "on_ground (T/F)" : {
          "type" : "text",
        },
        "velocity" : {
          "type" : "text",
        
        },
        "true_track" : {
          "type" : "text",
        },
        "vertical_rate" : {
          "type" : "text",
        },
        "sensors" : {
          "type" : "text",
        },
        "geo_altitude" : {
          "type" : "text",
        },
         "squawk" : {
          "type" : "text",
        },
        "spi" : {
          "type" : "text",
        },
        "position_source" : {
          "type" : "text",
        },
        
          }
        }


        try:
          es.indices.create(index='positions', mappings=mappings)
        except RequestError as es1:
          print("L'index positions existe déjà")
  
        print ("debut de chargement des positions dans elasticsearch") 
        helpers.bulk(es, list_dict_positions, index='positions',  request_timeout=200)
        
        print ("fin de chargement des positions dans elasticsearch")