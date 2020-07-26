#!/usr/bin/env python3

import sys
import click
import urllib.parse
import requests


@click.command()
@click.argument('address')
def get_weather(address):
    """GET WEATHER APP"""

    url = 'https://nominatim.openstreetmap.org/search/{}?format=json'.format(urllib.parse.quote(address))
    response = requests.get(url).json()
    latitude, longitude = response[0]["lat"], response[0]["lon"]

    # Getting location for current position
    # r = requests.get('https://api.ipdata.co?api-key=test').json()
    # latitude, longitude = r['latitude'], r['longitude']

    result = requests.get('https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={}&lon={}'.format(
        latitude, longitude
    ))
    print(result.json())


if __name__ == '__main__':
    get_weather()
