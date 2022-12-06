import random
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

import sys
# ajouter le chemin des scripts dans le container airflow
# Il faut d'abord ajouter ce volume dans le docker-compose 
sys.path.append('/opt/airflow/scripts/es')
from load_flight_data_in_elasticsearch import LoadFlightData
from extract_flight_data import FlightData

my_elastic_search_dag = DAG(
    dag_id='my_elastic_search_dag',
    schedule_interval="@daily",
    default_args={
        'owner': 'airflow',
        'start_date': datetime(2022, 12, 1, 8, 0, 0),
    },
    catchup=False
)

def random_fail_task():
    random.seed()
    a = random.randint(0, 100)
    print(a)
    if a > 20:
        raise Exception('This task randomly failed')


def successful_task():
    #time.sleep(10)
    print('success')

def extract(task_instance):
    user_name_opensky='rim-DE'
    password_opensky='bde_airlines'
    e = FlightData (user_name_opensky, password_opensky)
    dict_flights=e.extractFlightData ()
    task_instance.xcom_push(
        key="dict_flights",
        value=dict_flights
    )

def load(task_instance):
    dict_flights=task_instance.xcom_pull(
            key="dict_flights",
            task_ids=['ExtractFlights']
        )
    l=LoadFlightData ("http://elastic-search:9200")
    #connect to elasticsearch
    es=l.connect()
    #Chargement des vols dans elasticsearch
    l.load(es, dict_flights)

CheckElasticSearchConnexion = PythonOperator(
    task_id='CheckElasticSearchConnexion',
    python_callable=random_fail_task,
    retries=50,
    retry_delay=timedelta(seconds=5),
    dag=my_elastic_search_dag
)

DeleteOldDocumentsFromES = PythonOperator(
    task_id='DeleteOldDocumentsFromES',
    python_callable=successful_task,
    dag=my_elastic_search_dag,
    trigger_rule='all_success'
)

ExtractFlights = PythonOperator(
    task_id='ExtractFlights',
    python_callable=extract,
    dag=my_elastic_search_dag,
    trigger_rule='all_success'
)

LoadFlightsInES = PythonOperator(
    task_id='LoadFlightsInES',
    python_callable=load,
    dag=my_elastic_search_dag,
    trigger_rule='all_success'
)


CheckElasticSearchConnexion >> [DeleteOldDocumentsFromES, ExtractFlights]
ExtractFlights >> LoadFlightsInES