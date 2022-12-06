from elasticsearch import Elasticsearch, helpers, RequestError
import time
import json

class LoadFlightData :

    def __init__ (self, hosts):
        self.hosts = hosts
    
    def connect (self):
      es = Elasticsearch(hosts = self.hosts)
        
      return es

    def load(self, es, json_file):

      # Opening JSON file
      f = open(json_file)
  
      # returns JSON object as a dictionary
      json_data = json.load(f)

      
      print ("debut de chargement des données dans elasticsearch") 
      helpers.bulk(es, json_data, index='flights',  request_timeout=200)
      print ("fin de chargement des données dans elasticsearch")





    """
    def load_positions (self, es, list_dict_positions):
        mappings={
        "mappings":{
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
        }


        try:
          es.indices.create(index='positions', body=mappings)
        except RequestError as es1:
          print("L'index positions existe déjà")
  
        print ("debut de chargement des positions dans elasticsearch") 
        helpers.bulk(es, list_dict_positions, index='positions',  request_timeout=200)
        
        print ("fin de chargement des positions dans elasticsearch")
      """