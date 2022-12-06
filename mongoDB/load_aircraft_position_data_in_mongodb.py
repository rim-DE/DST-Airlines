import pprint
import json
from pymongo import MongoClient


class LoadPositionAircraftData :

    def __init__ (self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def connect (self):
        client = MongoClient(host= self.host, port=self.port, username=self.user, password=self.password)
        return client


    def load (self, client, json_file):
    
        # Opening JSON file
        f = open(json_file)
  
        # returns JSON object as 
        # a dictionary
        data = json.load(f)
        
        #La base de données ne sera crée que lors de la première insertion
        mydb = client['aircraft']
        mycol = mydb["positions"]       
        print ("debut de chargement des données dans mongodb") 

        mycol.insert_many(data)
        print ("fin de chargement des données dans mongodb")