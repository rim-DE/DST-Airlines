
import mysql.connector
import json
import os
import traceback 
import csv

class UpdateBase:

    def csv_to_tuples(self,csv_file):
        '''
        fonction qui importe un fichier csv et le transforme en liste de tuples
        input: fichier csv
        output: liste de tuples
        '''
        with open(csv_file) as f:
            reader = csv.reader(f)
            lst = list(tuple(line) for line in reader)
            lst=lst[2::]
        return lst 


    # fonction de connexion à la base
    def connection(self):
      try:
        #dbUrl = os.environ['DB_URL']
        mydb= mysql.connector.connect( host='airlines-mysql', user='root',password='123456', database="dstairlines")
      except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
      return mydb


      

    # fonction qui permet d'insérer les données scrappées du html dans la table 
    def insert_aeroport (self, list_of_tuples):
      try:
        #etablir la connexion
        mydb = self.connection() 
        mycursor = mydb.cursor()
        sql = "INSERT IGNORE INTO aeroports (ICAO, IATA, nom, taille, pays, ville) VALUES (%s, %s,%s, %s, %s, %s )"
        mycursor.executemany(sql, list_of_tuples)
        mydb.commit()
        print("table aeroports remplie!")
      
      except Exception:
        print(traceback.format_exc())
        mydb.rollback()
      
      finally:
        mycursor.close()
        mydb.close()
        print("connection MySQL est fermée")
      

    # récupérer les données des aéroports scrappées et les insérer
    #airport_tuples = csv_to_tuples("airport_csv.csv")
    #insert_aeroport(airport_tuples)


    ## récupérer les données des compagnies aériennes et les insérer
    def insert_compagnies (self,compagnies_tuples):
      try:
        #etablir la connexion
        mydb = self.connection() 
        mycursor = mydb.cursor()
        sql = "INSERT IGNORE INTO compagnies (icao24,registration,manufacturericao,manufacturername,model,serialnumber,ownername) VALUES (%s, %s,%s, %s, %s, %s , %s)"
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

    #compagnies_tuples = csv_to_tuples("clean_aircraft.csv")
    #print(compagnies_tuples[0:10])
    #insert_compagnies(compagnies_tuples)
