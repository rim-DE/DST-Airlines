from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import mysql.connector
import traceback 

import sys
sys.path.append('/opt/airflow/scripts/mysql')
from remplissage_mysqldb import UpdateBase
from html_scrapping import HTMLScrapping


mysql_dag = DAG(
    dag_id='mysql_dag',
    description='ETL mysql',
    tags=['dst-airlines'],
    schedule_interval='@monthly',
    #schedule_interval="0 0 1 * *"
    #schedule_interval=timedelta(minutes=20),
    default_args={
        'owner': 'airflow',
        'start_date': datetime(2022, 12, 1, 8, 0, 0),
    },
    catchup=False
    
)



def check_connexion():
    u = UpdateBase()
    u.connection()

def scrapping():
    s = HTMLScrapping()
    s.tuples_to_csv('airport_csv_3.csv')

def delete_airoports():
    try:
        u = UpdateBase()
        mydb=u.connection()
        mycursor = mydb.cursor()
        sql = "DELETE FROM aeroports"
        mycursor.execute(sql)
        mydb.commit()
        print("Contenu de la table aeroports supprimé!")
    
    except Exception:
        print(traceback.format_exc())
        mydb.rollback()
      
    finally:
        mycursor.close()
        mydb.close()
        print("connection MySQL est fermée")

def insert_scrapped_aeroports():
    s = HTMLScrapping()
    s.tuples_to_csv('airport_csv_3.csv')

    
    try: 
        u = UpdateBase()
        tuples = u.csv_to_tuples("airport_csv_3.csv")
        mydb=u.connection()
        mycursor = mydb.cursor()
        sql = "INSERT IGNORE INTO aeroports (ICAO, IATA, nom, taille, pays, ville) VALUES (%s, %s,%s, %s, %s, %s )"
        mycursor.executemany(tuples)
        mydb.commit()
        print("Table aeroports supprimé!")
    except Exception:
        print(traceback.format_exc())
        mydb.rollback()
      
    finally:
        mycursor.close()
        mydb.close()
        print("connection MySQL est fermée")



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
)

delete_airoports= PythonOperator(
    task_id='delete_airoports',
    python_callable=delete_airoports,
    retries=10,
    retry_delay=timedelta(seconds=10),
    dag=mysql_dag,
    trigger_rule='all_success'
)

insert_scrapped_aeroports = PythonOperator(
    task_id='insert_scrapped_aeroports',
    python_callable=insert_scrapped_aeroports,
    retries=10,
    retry_delay=timedelta(seconds=10),
    dag=mysql_dag,
    trigger_rule='all_success'
)

[CheckMysqlConnexion, htmlScrapping] >> delete_airoports >> insert_scrapped_aeroports