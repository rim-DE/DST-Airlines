from elasticsearch import Elasticsearch, helpers, RequestError
from elasticsearch.helpers import bulk, scan
from datetime import datetime, timedelta

class UpdateDataInES :

    def __init__ (self, hosts):
        self.hosts = hosts
    
    def connect (self):
      es = Elasticsearch(hosts = self.hosts)
        
      return es

    def deleteOldData(self, es):
        
        old_date = datetime.now() - timedelta(days=30)
                
        query_body = {
        "query": {
            "range": {
                "firstSeen": { 
                 "lte": old_date.strftime('%Y-%m-%d %H:%M:%S')
                }
            }
            }
            }
    

        bulk_deletes = []
        for result in scan(es,
                   query=query_body,  
                   index='flights',
                   _source=False,
                   track_scores=False,
                   scroll='5m'):
            result['_op_type'] = 'delete'
            bulk_deletes.append(result)

        bulk(es, bulk_deletes)