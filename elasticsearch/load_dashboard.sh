#!/bin/bash
curl -X POST localhost:5601/api/saved_objects/_import?createNewCopies=true -H "kbn-xsrf: true" --form file=@dashboard_dst_airlines_2.0.ndjson -H 'kbn-xsrf: true'
curl -X POST localhost:5601/api/saved_objects/_import?createNewCopies=true -H "kbn-xsrf: true" --form file=@dashboard_dst_airlines_2.1.ndjson -H 'kbn-xsrf: true'
