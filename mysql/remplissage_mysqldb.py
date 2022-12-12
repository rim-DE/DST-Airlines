
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

   
