#!/usr/bin/env python
# coding: utf-8


from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import string
import json
import csv



def extract_info():
    '''
    fonction qui permet de scrapper le site dont les aéroporte sont classifié par lettres alphabétique 
    et ensuite par page. 
    sortie: ensemble de données en liste
    '''
    #pour générer la liste des lettres de l'alphabet
    #list_alphabet = list(string.ascii_lowercase) 
    list_alphabet = ['a']
    #initialisation des listes des données 
    city_all = []
    country_all = []
    taille_all = []
    IATA_all = []
    ICAO_all = []
    name_all = []

    for alpha in list_alphabet:
    
        url_airport_1 = f"https://www.world-airport-codes.com/alphabetical/airport-code/{alpha}.html?page=1"
        page_1 = urlopen(url_airport_1)
        soup_1 = bs(page_1, "html.parser")
        airport_all = soup_1.findAll('a')
        #extarction des infos de la pages 1. Nous avons besoin de connaitre le nombre de pages par lettre
        #ex: les aéroports commençant par A sont sur 6 pages / les aéroports commençant par G sont sur 4 pages / etc...
        info_page_1 = [] 
        for j in range(len(airport_all)):
            info_page_1.append(airport_all[j].text)
    
        #nous remarquons le nombre de pages se trouvve dans la liste info_page_1 de la première page avant l'élément "›"
        info_utile = info_page_1.index("›")
        nb_pages = int(info_page_1[info_utile-1])
        
        for p in range(1, nb_pages+1):
            if p == 1:
                debut_scrap = info_utile+1
            elif p == nb_pages:
                debut_scrap = info_utile+1
            else :
                debut_scrap = info_utile+2
            
        
            url_airport_codes = f"https://www.world-airport-codes.com/alphabetical/airport-code/{alpha}.html?page={p}"
            page_i = urlopen(url_airport_codes)
            soup_i = bs(page_i, "html.parser")
        
            city = []
            country = []
            taille = []
            IATA = []
            ICAO = []
            name = []
        
            #extraction des infos des aéroports
            airport_info_all = soup_i.findAll('td')
        
            for j in range(1,len(airport_info_all),6):
                city.append(airport_info_all[j].text if airport_info_all[j].text == '' else airport_info_all[j].text.split(':')[1])
    
            for k in range(2,len(airport_info_all),6):
                country.append(airport_info_all[k].text if airport_info_all[k].text =='' else  airport_info_all[k].text.split(':')[1])
    
            for l in range(0,len(airport_info_all),6):
                taille.append(airport_info_all[l].text if airport_info_all[l].text == '' else airport_info_all[l].text.replace(' ','').split(':')[1].split('\n')[1])
    
            for m in range(3,len(airport_info_all),6):
                IATA.append(airport_info_all[m].text if airport_info_all[m].text =='' else airport_info_all[m].text.split(':')[1].split(' ')[1])
    
            for n in range(4,len(airport_info_all),6):
                ICAO.append(airport_info_all[n].text if airport_info_all[n].text == '' else airport_info_all[n].text.split(':')[1].split(' ')[1])

            #extraction des noms des aéroports
            airport_name_all = soup_i.findAll('a')
        
            for i in range(debut_scrap,(len(city)+debut_scrap)):
                name.append(airport_name_all[i].text if  airport_name_all[i].text == '' else airport_name_all[i].text)
            
            city_all.extend(city)
            country_all.extend(country)
            taille_all.extend(taille)
            IATA_all.extend(IATA)
            ICAO_all.extend(ICAO)
            name_all.extend(name)
            
            print(f'Scrapping de la page {alpha}-{p} réussie')
            
    return ICAO_all, IATA_all, name_all, taille_all, country_all ,city_all


def list_to_json(ICAO_all,IATA_all,name_all,country_all,city_all):
    '''
    créé un objet json à partir d'un ensemble de liste
    entrée: 5 listes des info
    sortie: un objet json les raassemblant et une liste des tuples
    '''
    list_dictionary_airport = []

    for i in range(len(ICAO_all)):
        dict= {"ICAO" : ICAO_all[i],
               "IATA" : IATA_all[i],
               "nom aeroport" : name_all[i],
               "pays" : country_all[i],
               "ville" : city_all[i]}
        list_dictionary_airport.append(dict)
        airport_json= json.dumps(list_dictionary_airport, indent=2)
    
    return airport_json

def list_to_tuples(ICAO_all,IATA_all,name_all,taille_all,country_all,city_all):
    airport_tuples = list(zip(ICAO_all,IATA_all,name_all,taille_all,country_all,city_all))
    return airport_tuples

def scrap_aeroport_data ():
    ICAO_all, IATA_all, name_all, taille_all, country_all ,city_all = extract_info()
    airport_tuples = list_to_tuples(ICAO_all, IATA_all, name_all, taille_all, country_all ,city_all)
    return airport_tuples
     
def tuples_to_csv(csv_file):
    # get aireport information sous forme de list de tuples
    data = scrap_aeroport_data ()
    # sauvegarder les tuples dans un fichier csv
    with open(csv_file,'w') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['ICAO','IATA', 'NOM', 'TAILLE', 'PAYS', 'CITE'])
        for mytuple in data:
            csv_out.writerow(mytuple)

# appel de la fonction tuples_to_csv
tuples_to_csv('airport_csv')






