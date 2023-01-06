#!/bin/bash

##enrich flights index
### step1: create 3 enrich policies
curl -XPUT "http://localhost:9200/_enrich/policy/icao24-policy" -H 'Content-Type: application/json' -d'
{
  "match": {
    "indices": "companies",
    "match_field": "icao24",
    "enrich_fields": ["ownername", "manufacturername", "model","icao24"]
  }
}'

curl -XPUT "http://localhost:9200/_enrich/policy/icao-policy" -H 'Content-Type: application/json' -d'
{
  "match": {
    "indices": "airports",
    "match_field": "icao",
    "enrich_fields": ["ville", "nom", "taille","pays"]
  }
}'



### step2: execute the policies 
curl -XPOST "http://localhost:9200/_enrich/policy/icao24-policy/_execute"
curl -XPOST "http://localhost:9200/_enrich/policy/icao-policy/_execute"


### step3: configure 3 pipelines

#1- configure icao24_lookup pipeline to match companies icao24 to flights icao 24
curl -XPUT "http://localhost:9200/_ingest/pipeline/icao24_lookup" -H 'Content-Type: application/json' -d'
{
  "description" : "Enriching flights details with companies data",
  "processors" : [
    {
      "enrich" : {
        "policy_name": "icao24-policy",
        "field" : "icao24",
        "target_field": "aircraft",
        "max_matches": "1"
      }
    },
    {
      "remove": {
        "field": ["icao24","estDepartureAirportHorizDistance", "estDepartureAirportVertDistance", "estArrivalAirportHorizDistance", "estArrivalAirportVertDistance", "departureAirportCandidatesCount", "arrivalAirportCandidatesCount"]
      }
    }
  ]
}'

#2- configure icao_departure_lookup pipeline to match airports icao to flights estDepartureAirport
curl -XPUT "http://localhost:9200/_ingest/pipeline/icao_departure_lookup" -H 'Content-Type: application/json' -d'
{
  "description" : "Enriching flights details with departure airports data",
  "processors" : [
    {
      "enrich" : {
        "policy_name": "icao-policy",
        "field" : "estDepartureAirport",
        "target_field": "DepartureAirport",
        "max_matches": "1"
      }
    },
    {
      "remove": {
        "field": ["estDepartureAirport"]
      }
    }
  ]
}'

#3- configure icao_arrival_lookup pipeline to match airports icao to flights estArrivalAirport
curl -XPUT "http://localhost:9200/_ingest/pipeline/icao_arrival_lookup" -H 'Content-Type: application/json' -d'
{
  "description" : "Enriching flights details with arrival airports data",
  "processors" : [
    {
      "enrich" : {
        "policy_name": "icao-policy",
        "field" : "estArrivalAirport",
        "target_field": "ArrivalAirport",
        "max_matches": "1"
      }
    },
    {
      "remove": {
        "field": ["estArrivalAirport"]
      }
    }
  ]
}'


### step4: apply enrichments with reindex APIs

curl -XPOST "http://localhost:9200/_reindex" -H 'Content-Type: application/json' -d'
{
  "source": {
    "index": "flights"
  },
  "dest": {
    "index": "flights1",
    "pipeline": "icao24_lookup"
  }
}'

curl -XPOST "http://localhost:9200/_reindex" -H 'Content-Type: application/json' -d'
{
  "source": {
    "index": "flights1"
  },
  "dest": {
    "index": "flights2",
    "pipeline": "icao_departure_lookup"
  }
}'

curl -XPOST "http://localhost:9200/_reindex" -H 'Content-Type: application/json' -d'
{
  "source": {
    "index": "flights2"
  },
  "dest": {
    "index": "flights3",
    "pipeline": "icao_arrival_lookup"
  }
}'



#we reindex the data because the data are not in an appropriate format
### step5: create an index with

curl -XPUT "http://localhost:9200/flights_enriched" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 1
  },
  "mappings" : {
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
  }'

curl -XPOST "http://localhost:9200/_reindex" -H 'Content-Type: application/json' -d'
{
  "source": {
    "index": "flights3"
  },
  "dest": {
    "index": "flights_enriched"
  }
}'


### step6: delete policies , pipelines and transitional indexes
curl -XDELETE "http://localhost:9200/_ingest/pipeline/icao24_lookup"
curl -XDELETE "http://localhost:9200/_ingest/pipeline/icao_departure_lookup"
curl -XDELETE "http://localhost:9200/_ingest/pipeline/icao_arrival_lookup"
curl -XDELETE "http://localhost:9200/_ingest/pipeline/location_arrival_lookup"
curl -XDELETE "http://localhost:9200/_ingest/pipeline/location_departure_lookup"
curl -XDELETE "http://localhost:9200/_enrich/policy/location-policy"
curl -XDELETE "http://localhost:9200/_enrich/policy/icao24-policy"
curl -XDELETE "http://localhost:9200/_enrich/policy/icao-policy"
curl -XDELETE "http://localhost:9200/flights1"
curl -XDELETE "http://localhost:9200/flights2"
curl -XDELETE "http://localhost:9200/flights3"


## empty flights index
curl -XPOST "http://localhost:9200/flights/_delete_by_query" -H 'Content-Type: application/json' -d'
{
  "query": { 
    "match_all": {}
  }
}'


## set kibana dashboard up
curl -X POST "http://localhost:5601/api/saved_objects/_import?overwrite=true" -H "kbn-xsrf: true" --form file=@dashboard_dst_airlines_2.0.ndjson -H 'kbn-xsrf: true'
