import random
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch


import sys
# ajouter le chemin des scripts dans le container airflow
# Il faut d'abord ajouter ce volume dans le docker-compose 
sys.path.append('/opt/airflow/scripts/es')
from load_flight_data_in_elasticsearch import LoadFlightData
from extract_flight_data import FlightData
from update_data_in_elastic_search import UpdateDataInES

my_elastic_search_dag = DAG(
    dag_id='my_elastic_search_dag',
    tags=['dst-airlines'],
    schedule_interval="0 8 * * *",
    default_args={
        'owner': 'airflow',
        'start_date': datetime(2022, 12, 1, 8, 0, 0),
    },
    
)



def check_connexion ():
    es = Elasticsearch(hosts = "http://elastic-search:9200")
    try:
        es.ping()
        if (es.cluster.health()['status'] not in ['yellow','green']):
            raise Exception('Connexion elasticSearch non disponible')
    except Exception:
        print ('Connexion elasticSearch non disponible')

def delete():
    u=UpdateDataInES ("http://elastic-search:9200")
    #se connecter à elasticsearch
    es=u.connect()
    #supprimer les anciens documents
    u.deleteOldData (es)

def extract():
    user_name_opensky='rim-DE'
    password_opensky='bde_airlines'
    e = FlightData (user_name_opensky, password_opensky)
    e.extractFlightData ('flights.json')
    

def load():
    l=LoadFlightData ("http://elastic-search:9200")
    #se connecter à elasticsearch
    es=l.connect()
    #Chargement des vols dans elasticsearch
    l.load(es, 'flights.json')

CheckElasticSearchConnexion = PythonOperator(
    task_id='CheckElasticSearchConnexion',
    python_callable=check_connexion,
    retries=50,
    retry_delay=timedelta(seconds=5),
    dag=my_elastic_search_dag
)

DeleteOldDocumentsFromES = PythonOperator(
    task_id='DeleteOldDocumentsFromES',
    python_callable=delete,
    dag=my_elastic_search_dag,
    retries=10,
    retry_delay=timedelta(seconds=10),
    trigger_rule='all_success'
)

ExtractFlights = PythonOperator(
    task_id='ExtractFlights',
    python_callable=extract,
    dag=my_elastic_search_dag,
    retries=10,
    retry_delay=timedelta(seconds=10),
    trigger_rule='all_success'
)

LoadFlightsInES = PythonOperator(
    task_id='LoadFlightsInES',
    python_callable=load,
    dag=my_elastic_search_dag,
    retries=10,
    retry_delay=timedelta(seconds=10),
    trigger_rule='all_success'
)

ExtractFlights >> LoadFlightsInES
CheckElasticSearchConnexion >> [DeleteOldDocumentsFromES, LoadFlightsInES]
