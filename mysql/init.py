
import mysql.connector
import json
import os
import traceback 
import csv
from remplissage_mysqldb import UpdateBase

# instantiation de la classe
u = UpdateBase()



# initialisation de la table compagnies aériennes

#transformer le fichier csv en tuples
with open("clean_aircraft.csv") as f:
    reader = csv.reader(f)
    compagnies_tuples = list(tuple(line) for line in reader)
    compagnies_tuples=compagnies_tuples[2::]
    print(compagnies_tuples[:3])


# insérer les données dans la table 
try:
    #etablir la connexion
    mydb = u.connection() 
    mycursor = mydb.cursor()
    sql="""INSERT INTO compagnies (icao24,registration,manufacturericao,manufacturername,model,serialnumber,ownername) VALUES (%s, %s,%s, %s, %s, %s , %s) ON DUPLICATE KEY UPDATE registration=VALUES(registration),  manufacturericao=VALUES(manufacturericao), manufacturername=VALUES(manufacturername), model=VALUES(model), serialnumber=VALUES(serialnumber),ownername=VALUES(ownername)"""
    mycursor.executemany(sql, compagnies_tuples)
    mydb.commit()
    print("table compagnies remplie!")
      
except Exception:
    print(traceback.format_exc())
    mydb.rollback()
      
finally:
    mycursor.close()
    mydb.close()
    print("connection MySQL est fermé")


# initialisation de la table aeroport

with open("airport_csv.csv") as f:
    reader = csv.reader(f)
    aeroport_tuples = list(tuple(line) for line in reader)
    aeroport_tuples=aeroport_tuples[2::]
    print(aeroport_tuples[:3])


# insérer les données dans la table aeroport
try:
    #etablir la connexion
    mydb = u.connection() 
    mycursor = mydb.cursor()
    sql="""INSERT IGNORE INTO aeroports (ICAO, IATA, nom, taille, pays, ville) VALUES (%s, %s,%s, %s, %s, %s)"""
    mycursor.executemany(sql, aeroport_tuples)
    mydb.commit()
    print("table aeroport remplie!")
      
except Exception:
    print(traceback.format_exc())
    mydb.rollback()
      
finally:
    mycursor.close()
    mydb.close()
    print("connection MySQL est fermé")