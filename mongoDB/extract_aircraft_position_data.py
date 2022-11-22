import pprint

import requests


class OpenSkyClient:
    """
        A helper class to get flights data from open-sky api.
    """
    ROOT_URL = 'https://opensky-network.org/api/'
    TRACK_FLIGHT_URI = 'tracks/all'
    FIND_ALL = 'flights/all'

    def track_flight(self, flight_icao24):
        """
            tracks a flight with the icao24 code.

        Args:
            flight_icao24: the icao24 code

        Returns:
            flight_data: returns the flight data or empty dictionary in case of http error.
        """
        query_params = {
            "icao24": flight_icao24
        }

        response = requests.get(self.ROOT_URL + self.TRACK_FLIGHT_URI, params=query_params)
        if response.status_code != 200:
            pprint.pp(response)
            return {}

        return response.json()

    def all_flights(self, begin, end):
        """
            gets all flights information (no tracking data).

        Args:
            begin: the start date in Unix epoch time (timestamp)
            end: the end date in Unix epoch time (timestamp)

        Returns:
            flights_information: a list of flights information.
        """
        params = {
            "begin": begin,
            "end": end
        }
        response = requests.get(self.ROOT_URL + self.FIND_ALL, params=params)
        if response.status_code != 200:
            pprint.pp(response)
            return {}

        return response.json()
