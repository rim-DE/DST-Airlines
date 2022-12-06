import pprint
import pandas as pd
import requests
import json

#L'extraction des positions des avions doit se faire toute les 45 secondes
class PositionAircraftData:
    
    def __init__ (self, user_name, password):
        
        self.user_name = user_name
        self.password = password

    def extractPositionAircrafttData (self, fileName):

        """
            retourne les positions de tous les avions 
            en temps réel
        """
        OpenSky_url = 'https://'+self.user_name+':'+self.password+'@opensky-network.org/api/states/all'
        positions_data = requests.get (OpenSky_url)

        if positions_data.status_code != 200:
            pprint.pp(positions_data)
            return {}
        
        try:
            columns = ['icao24','callsign','origin_country','time_position','last_contact','long','lat','baro_altitude','on_ground (T/F)','velocity','true_track','vertical_rate','sensors',
            'geo_altitude','squawk','spi','position_source','category']
            flight_df=pd.DataFrame(positions_data.json()['states'],columns=columns)
        except ValueError:
            columns = ['icao24','callsign','origin_country','time_position','last_contact','long','lat','baro_altitude','on_ground (T/F)','velocity','true_track','vertical_rate','sensors',
            'geo_altitude','squawk','spi','position_source']
            flight_df=pd.DataFrame(positions_data.json()['states'],columns=columns)

            #flight_df ['time_position'] = flight_df ['time_position'].apply (lambda tp : str(datetime.fromtimestamp(tp)))
            #flight_df ['last_contact'] = flight_df ['last_contact'].apply (lambda tp : str(datetime.fromtimestamp(tp)))
            
            dict_positions = flight_df.to_dict('records')

            with open (fileName, 'w') as f:
                json.dump(dict_positions, f)
            #print (f.name)
        
    
