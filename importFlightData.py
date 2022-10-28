import pandas as pd
import requests
import json

OpenSky_url = 'https://opensky-network.org/api/states/all'
OpenSky_data = requests.get(OpenSky_url).json()

try:
    columns = ['icao24','callsign','origin_country','time_position','last_contact','long','lat','baro_altitude','on_ground (T/F)','velocity','true_track','vertical_rate','sensors',
    'geo_altitude','squawk','spi','position_source','category']
    flight_df=pd.DataFrame(OpenSky_data['states'],columns=columns)
    flight_df=flight_df.fillna('No Data')
except ValueError:
    columns = ['icao24','callsign','origin_country','time_position','last_contact','long','lat','baro_altitude','on_ground (T/F)','velocity','true_track','vertical_rate','sensors',
    'geo_altitude','squawk','spi','position_source']
    flight_df=pd.DataFrame(OpenSky_data['states'],columns=columns)
    flight_df=flight_df.fillna('No Data')

print (flight_df)

