from FlightRepository import FlightRepository
from OpenSkyClient import OpenSkyClient

client = OpenSkyClient()
flight_data = client.track_flight('4b1b1b')

repo = FlightRepository()
repo.save_flight(flight_data)

