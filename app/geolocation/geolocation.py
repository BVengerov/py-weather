import urllib.parse
import requests


class Geolocation:
    @classmethod
    def get_coordinates_for_address(cls, address):
        url = 'https://nominatim.openstreetmap.org/search/{}?format=json'.format(urllib.parse.quote(address))
        response = requests.get(url)
        response.raise_for_status()
        payload = response.json()
        return payload[0]["lon"], payload[0]["lat"]

    @classmethod
    def get_coordinates_by_ip(cls):
        print('Getting location for the current position...')
        response = requests.get('https://api.ipdata.co?api-key=test')
        response.raise_for_status()
        payload = response.json()
        return payload['longitude'], payload['latitude']

    @classmethod
    def get_location_name_by_coordinates(cls, longitude, latitude):
        url = 'https://nominatim.openstreetmap.org/reverse/?lon={}&lat={}&zoom=14&format=json'.format(
            longitude, latitude
        )
        response = requests.get(url)
        response.raise_for_status()
        return response.json()['display_name']