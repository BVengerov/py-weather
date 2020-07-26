#!/usr/bin/env python3
import json
import sys
import urllib.parse
import requests


def get_coordinates(address: str) -> tuple:
    if not address:
        print('Getting location for the current position...')
        response = requests.get('https://api.ipdata.co?api-key=test')
        response.raise_for_status()
        payload = response.json()
        latitude, longitude = payload['latitude'], payload['longitude']
    else:
        headers = {
            'User-Agent': 'py-weather github.com/BVengerov/py-weather',
        }
        url = 'https://nominatim.openstreetmap.org/search/{}?format=json'.format(urllib.parse.quote(address))
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        payload = response.json()
        latitude, longitude = payload[0]["lat"], payload[0]["lon"]
    return round(float(latitude), 4), round(float(longitude), 4)


def print_current_weather(results):
    timeserie = results['properties']['timeseries'][0]
    forecast_time = timeserie['time']
    weather = timeserie['data']['instant']['details']
    temp = weather['air_temperature']
    humidity = weather['relative_humidity']
    wind_speed = weather['wind_speed']
    report = '''Current weather conditions: \n
        Temperature: {}C
        Humidity: {}
        Wind speed: {}
        Weather got at {}
    '''.format(
        temp, humidity, wind_speed, forecast_time
    )
    print(report)


def get_weather(address: str):
    """GET WEATHER APP"""

    response = requests.get('https://api.met.no/weatherapi/locationforecast/2.0/complete?lat={}&lon={}'.format(
        *get_coordinates(address)
    ))

    response.raise_for_status()
    print_current_weather(response.json())
    # print(parse_close_weather(response.json()))
    # print(parse_farther_weather(response.json()))


if __name__ == '__main__':
    try:
        address = sys.argv[1]
    except IndexError:
        address = ''
    get_weather(address)
