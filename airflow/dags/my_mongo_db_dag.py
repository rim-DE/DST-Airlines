import random
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

import sys
# ajouter le chemin des scripts défini dans le container airflow à l'interpréteur python
# Il faut d'abord ajouter ce volume dans le docker-compose 
sys.path.append('/opt/airflow/scripts/mongo')
from extract_aircraft_position_data import PositionAircraftData
from load_aircraft_position_data_in_mongodb import LoadPositionAircraftData

my_mongo_db_dag = DAG(
    dag_id='my_mongo_db_dag',
    tags=['dst-airlines'],
    schedule_interval=timedelta(seconds=45),
    default_args={
        'owner': 'airflow',
        'start_date': datetime(2022, 12, 1, 8, 0, 0),
    },
    catchup=False
)

def successful_task():
    #time.sleep(10)
    print('success')

def check_connexion ():
    host = "my_mongo"
    port = 27017
    user = 'admin'
    password = 'pass'

    myclient = MongoClient(host=host, port=port, username=user, password=password)
    try:
        myclient.admin.command('ping')
    except ConnectionFailure:
        print("Connexion mongoDB non disponible")

def extract():
    user_name_opensky='rim-DE'
    password_opensky='bde_airlines'
    p = PositionAircraftData (user_name_opensky, password_opensky)
    p.extractPositionAircrafttData ('positions.json')
    

def load():
    l=LoadPositionAircraftData ("my_mongo", 27017, 'admin', 'pass')
    #se connecter à mongodb
    cl=l.connect()
    #Chargement des positions dans mongodb
    l.load(cl, 'positions.json')

CheckMongoDBConnexion = PythonOperator(
    task_id='CheckMongoDBConnexion',
    python_callable=check_connexion,
    retries=50,
    retry_delay=timedelta(seconds=5),
    dag=my_mongo_db_dag
)

ExtractPositions = PythonOperator(
    task_id='ExtractPositions',
    python_callable=extract,
    dag=my_mongo_db_dag,
    retries=10,
    retry_delay=timedelta(seconds=5),
    trigger_rule='all_success'
)

LoadPositionsInMongoDB = PythonOperator(
    task_id='LoadPositionsInMongoDB',
    python_callable=load,
    dag=my_mongo_db_dag,
    retries=10,
    retry_delay=timedelta(seconds=5),
    trigger_rule='all_success'
)


CheckMongoDBConnexion >> ExtractPositions >> LoadPositionsInMongoDB