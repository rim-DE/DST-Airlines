from elasticsearch import Elasticsearch, RequestError
import time

hosts = "http://localhost:9200"
#hosts = "http://elastic-search:9200"
"""
while True:
    es = Elasticsearch(hosts = hosts)
    if es.ping():
        if (es.cluster.health()['status'] in ['yellow','green']):
            break
    time.sleep(5)
"""
es = Elasticsearch(hosts = hosts)

mappings_flights = {
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
      

index_name = 'flights'
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, mappings=mappings_flights)


mappings_airports = {
      "properties" : {
        "iCAO" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword"
            }
          }
        },
        "IATA" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword"
            }
          }
        },
        "Nom" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword"
            }
          }
        },
        "Taille" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword"
            }
          }
        },
        "Pays" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword"
            }
          }
        },
        "Ville" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword"
            }
          }
        }
      }
    }

index_name = 'airports'
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, mappings=mappings_airports)


mappings_companies = {
        "properties" : {
          "icao24" : {
            "type" : "text",
            "fields" : {
              "keyword" : {
                "type" : "keyword"
              }
            }
          },
          "registration" : {
            "type" : "text",
            "fields" : {
              "keyword" : {
                "type" : "keyword"
              }
            }
          },
          "manufacturericao" : {
            "type" : "text",
            "fields" : {
              "keyword" : {
                "type" : "keyword"
              }
            }
          },
          "manufacturername" : {
            "type" : "text",
            "fields" : {
              "keyword" : {
                "type" : "keyword"
              }
            }
          },
          "model" : {
            "type" : "text",
            "fields" : {
              "keyword" : {
                "type" : "keyword"
              }
            }
          },
          "serialnumber" : {
            "type" : "text",
            "fields" : {
              "keyword" : {
                "type" : "keyword"
              }
            }
          },
          "ownername" : {
            "type" : "text",
            "fields" : {
              "keyword" : {
                "type" : "keyword"
              }
            }
          }
        }
      }

index_name = 'companies'
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, mappings=mappings_companies)


mappings_flights_enriched = {
    "properties" : {
        "ArrivalAirport" : {
          "properties" : {
            "icao" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword"
                }
              }
            },
            "nom" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword"
                }
              }
            },
            "pays" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword"
                }
              }
            },
            "taille" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword"
                }
              }
            },
            "ville" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword"
                }
              }
            }
          }
        },
        "DepartureAirport" : {
          "properties" : {
            "icao" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword"
                }
              }
            },
            "nom" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword"
                }
              }
            },
            "pays" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword"
                }
              }
            },
            "taille" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword"
                }
              }
            },
            "ville" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword"
                }
              }
            }
          }
        },
        "aircraft" : {
          "properties" : {
            "icao24" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword"
                }
              }
            },
            "manufacturername" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword"
                }
              }
            },
            "model" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword"
                }
              }
            },
            "ownername" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword"
                }
              }
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
        "firstSeen" : {
          "type" : "date",
          "format" : "yyyy-MM-dd HH:mm:ss"
        },
        "lastSeen" : {
          "type" : "date",
          "format" : "yyyy-MM-dd HH:mm:ss"
        }
      }
    }

index_name = 'flights_enriched'
if not es.indices.exists(index=index_name):
  es.indices.create(index=index_name, mappings=mappings_flights_enriched)


print ("Connexion à elastic-search réussie!")
print ("Création de l'index flights s'il n'existe pas!")
