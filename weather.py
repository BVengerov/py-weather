#!/usr/bin/env python3
import json
import sys
import urllib.parse
import requests


def get_coordinates(address: str) -> tuple:
    if not address:
        print('Getting location for current position')
        r = requests.get('https://api.ipdata.co?api-key=test').json()
        latitude, longitude = r['latitude'], r['longitude']
    else:
        url = 'https://nominatim.openstreetmap.org/search/{}?format=json'.format(urllib.parse.quote(address))
        response = requests.get(url).json()
        latitude, longitude = response[0]["lat"], response[0]["lon"]
    return round(float(latitude), 4), round(float(longitude), 4)


def parse_current_weather(results):
    print(results)


def get_weather(address: str):
    """GET WEATHER APP"""

    result = requests.get('https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={}&lon={}'.format(
        *get_coordinates(address)
    ))

    print(parse_current_weather(result.json()))
    # print(parse_close_weather(result.json()))
    # print(parse_farther_weather(result.json()))


if __name__ == '__main__':
    try:
        address = sys.argv[1]
    except IndexError:
        address = ''
    get_weather(address)
