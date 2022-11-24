import pprint

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


    def load (self, client, dict_positions):
    
        list_of_db = client.list_database_names()
 
        
        #La base de données ne sera crée que lors de la première insertion
        mydb = client['aircraft']
        
        mycol = mydb["positions"]       
        print ("debut de chargement des données dans mongodb") 
        mycol.insert_many(dict_positions)
        print ("fin de chargement des données dans mongodb")