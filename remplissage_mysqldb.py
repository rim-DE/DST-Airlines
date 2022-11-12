
import mysql.connector
import json
import html_scrapping

# fonction de connexion à la base
def connection():
  mydb= mysql.connector.connect( host="localhost",user="root",password="123456", database="dstairlines")
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
  except:
    print("Erreur!!")
    mydb.rollback()
  finally:
    mycursor.close()
    mydb.close()
    print("connection MySQL est fermé")
  

# récupérer les données des aéroports scrappées et les insérer
airport_tuples = html_scrapping.scrap_aeroport_data()
insert_aeroport(airport_tuples)


#to do: 

# fonction qui récupère un fichier csv propre

## récupérer les données des compagnies aériennes et les insérer
# compagnies_tuples = html_scrapping.csv_to_tuples()
'''
def insert_compagnies (list_of_tuples):
  sql = "INSERT INTO compagnies (icao24,registration, manufacturericao, manufacturername, model, typecode, /
  serialnumber, linenumber, icaoaircrafttype, operator, operatorcallsign, operatoricao, operatoriata, owner, testreg, registered, reguntil, status, built, firstflightdate, seatconfiguration, engines, modes, adsb, acars, notes, categoryDescription/
  VALUES (%s, %s,%s, %s, %s, %s )"
  mycursor.executemany(sql, list_of_tuples)
  mydb.commit()
  '''
# insert_compagnies(compagnies_tuples)
