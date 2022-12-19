#!/bin/bash
curl -X POST localhost:5601/api/saved_objects/_import?createNewCopies=true -H "kbn-xsrf: true" --form file=@dashboard_dst_airlines.ndjson -H 'kbn-xsrf: true'
