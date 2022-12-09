from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import mysql.connector

import sys
sys.path.append('/opt/airflow/scripts/mysql')
from remplissage_mysqldb import connection, insert_aeroport
from html_scrapping import HTMLScrapping


mysql_dag = DAG(
    dag_id='mysql_dag',
    description='ETL mysql',
    tags=['dst-airlines'],
    schedule_interval=timedelta(minutes=20),
    default_args={
        'owner': 'airflow',
        'start_date': datetime(2022, 12, 1, 8, 0, 0),
    },
    catchup=False
    
)



'''
def update_base():
    print('update_mysql base')



def scrapping():
    tuples_to_csv('airport_csv')

CheckMysqlConnexion = PythonOperator(
    task_id='CheckMysqlConnexion',
    python_callable=check_connexion,
    retries=50,
    retry_delay=timedelta(seconds=30),
    dag=mysql_dag
)



htmlScrapping = PythonOperator(
    task_id='htmlScrapping',
    python_callable=scrapping,
    
    dag=mysql_dag
)


updateBase = PythonOperator(
    task_id='updateBase',
    python_callable=insert_aeroport,
    dag=mysql_dag
)


htmlScrapping

'''
def check_connexion ():
    #dbUrl = os.environ['DB_URL']
    #host = dbUrl
    user = 'root'
    password = '123456'
    try:
        mydb= mysql.connector.connect( host='airlines-mysql', user=user,password=password, database="dstairlines")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))


def scrapping():
    s = HTMLScrapping ()
    s.tuples_to_csv('airport_csv_3.csv')


CheckMysqlConnexion = PythonOperator(
    task_id='CheckMysqlConnexion',
    python_callable=check_connexion,
    retries=50,
    retry_delay=timedelta(seconds=5),
    dag=mysql_dag
)


htmlScrapping = PythonOperator(
    task_id='htmlScrapping',
    python_callable=scrapping,
    retries=10,
    retry_delay=timedelta(seconds=10),
    dag=mysql_dag,
    trigger_rule='all_success'
)


CheckMysqlConnexion >> htmlScrapping