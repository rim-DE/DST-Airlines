import pprint

from pymongo import MongoClient


def transform_flight(source_format_flight):
    keys = ['time', 'latitude', 'longitude', 'baro_altitude', 'true_track', 'on_ground']

    new_format_flight = {
        "icao24": source_format_flight.get('icao24'),
        "callsign": source_format_flight.get('callsign'),
        "startTime": source_format_flight.get('startTime'),
        "endTime": source_format_flight.get('endTime'),
        "path": []
    }

    for p in source_format_flight.get('path'):
        new_format_flight['path'].append(dict(zip(keys, p)))

    return new_format_flight


class FlightRepository:
    """
        This class saves and gets data from the mongo-db database
    """
    DATABASE_NAME = 'aviation'
    FLIGHT_COLLECTION = 'flights'

    def __init__(self):
        mongo_client = MongoClient('mongodb://localhost:27017/', username='soukaina', password='JK3L2JKL')
        self.flights_collection = mongo_client.get_database(self.DATABASE_NAME).get_collection(self.FLIGHT_COLLECTION)

    def save_flight(self, flight):
        """
        transforms and saves a flight's data into the flights collection in mongo-db.
        Args:
            flight: the flight data from open-sky api to be saved. 
        """
        new_format_flight = transform_flight(flight)
        self.flights_collection.insert_one(new_format_flight)
