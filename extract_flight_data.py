import pandas as pd
import requests
import json
import pprint
from datetime import datetime, timedelta

#Les vols sont mis à jour par un traitement batch la nuit, c'est-à-dire que seuls les vols de la veille ou d'avant sont disponibles.

# Il faut automatiser l'extraction et le chargement dans les bases elastic et mongo en définissant un cron tab par exemple
# il faut exécuter le script tous les jours à 8h de matin (par exemple)


# strftime convert date to string
# strptime convert string to date


# on définit la date de début

begin_date = datetime.strptime(datetime.strftime(datetime.now() - timedelta(2), '%Y-%m-%d'), '%Y-%m-%d')
begin_date += timedelta(hours=20, minutes=00) 

end = datetime.strptime(datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d'), '%Y-%m-%d')
end += timedelta(hours=18, minutes=00) 

user_name='rim-DE'
password='bde_airlines'

dict_flights = {
    'flight' : []
}

# Extract data from Opensky API
# on ne peut récupérer les données que par plage de deux heures
i=0
while (begin_date <= end):
    end_date = begin_date + timedelta(hours=2)
    timestamp_begin_date = int(datetime.timestamp(begin_date))
    timestamp_end_date = int(datetime.timestamp(end_date))
    OpenSky_url = 'https://'+user_name+':'+password+'@opensky-network.org/api/flights/all?begin='+str(timestamp_begin_date)+'&end='+str(timestamp_end_date)
    flights_data = requests.get(OpenSky_url).json()
    #Traansformer les timestamps en dates
    #begin_date = end_date + timedelta(hours=1)
    begin_date = end_date 

   
    
    for flight in flights_data:
        flight ['firstSeen'] = str(datetime.fromtimestamp(flight ['firstSeen']))
        flight ['lastSeen'] = str(datetime.fromtimestamp(flight ['lastSeen']))
    dict_flights['flight'].extend(flights_data)
    
#exporter l'ensemble des données extraites dans un fichier json
    with open ('flights_data.json', 'w') as f:
        json.dump(dict_flights, f)
