
import mysql.connector
import json
import os
import traceback 
import csv
from remplissage_mysqldb import UpdateBase

# instantiation de la classe
u = UpdateBase()


#transformer le fichier csv en tuples
with open("clean_aircraft.csv") as f:
    reader = csv.reader(f)
    aircraft_tuples = list(tuple(line) for line in reader)
    aircraft_tuples=aircraft_tuples[2::]
    print(aircraft_tuples[:3])


# insérer les tuples des compagnies aériennes dans la base
try:
    #etablir la connexion
    mydb = u.connection() 
    mycursor = mydb.cursor()
    sql="""INSERT INTO compagnies (icao24,registration,manufacturericao,manufacturername,model,serialnumber,ownername) VALUES (%s, %s,%s, %s, %s, %s , %s) ON DUPLICATE KEY UPDATE registration=VALUES(registration),  manufacturericao=VALUES(manufacturericao), manufacturername=VALUES(manufacturername), model=VALUES(model), serialnumber=VALUES(serialnumber),ownername=VALUES(ownername)"""
    mycursor.executemany(sql, aircraft_tuples)
    mydb.commit()
    print("table compagnies remplie!")
      
except Exception:
    print(traceback.format_exc())
    mydb.rollback()
      
finally:
    mycursor.close()
    mydb.close()
    print("connection MySQL est fermé")


