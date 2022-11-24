
import mysql.connector
import json
import html_scrapping as html_scrapping
import os
import traceback 

# fonction de connexion à la basls e
def connection():
  dbUrl = os.environ['DB_URL']
  #if(dbUrl == None):
  #  dbUrl = 'localhost'
  print("!!!!!!!!!!!!!!!!!!!!!!!!dbUrl: ", dbUrl)
  mydb= mysql.connector.connect( host=dbUrl, user="root",password="123456", database="dstairlines")
  return mydb

# fonction qui permet d'insérer les données scrappées du html dans la table 
def insert_aeroport (list_of_tuples):
  try:
    #etablir la connexion
    mydb = connection() 
    mycursor = mydb.cursor()
    
    sql = "INSERT INTO aeroports (ICAO, IATA, nom, taille, pays, ville) VALUES (%s, %s,%s, %s, %s, %s )"
    mycursor.executemany(sql, list_of_tuples)
    mydb.commit()
  
  except Exception:
    print(traceback.format_exc())
    mydb.rollback()
  
  finally:
    mycursor.close()
    mydb.close()
    print("connection MySQL est fermé")
  

# récupérer les données des aéroports scrappées et les insérer
airport_tuples = html_scrapping.scrap_aeroport_data()
insert_aeroport(airport_tuples)


# fonction qui récupère un fichier csv propre

## récupérer les données des compagnies aériennes et les insérer

def insert_compagnies (compagnies_tuples):
  try:
    #etablir la connexion
    mydb = connection() 
    mycursor = mydb.cursor()
    sql = "INSERT INTO compagnies (icao24,registration,manufacturericao,manufacturername,model,serialnumber,ownername) VALUES (%s, %s,%s, %s, %s, %s , %s)"
    sample_rows = compagnies_tuples[0:10]
    mycursor.executemany(sql, compagnies_tuples)
    mydb.commit()
  
  except Exception:
    print(traceback.format_exc())
    mydb.rollback()
  
  finally:
    mycursor.close()
    mydb.close()
    print("connection MySQL est fermé")

compagnies_tuples = html_scrapping.csv_to_tuples('clean_aircraft.csv')
print(compagnies_tuples[0:6])
insert_compagnies(compagnies_tuples)
