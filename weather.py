#!/usr/bin/env python3
import arrow
import sys
import urllib.parse
import requests


def get_coordinates(address_input: str) -> tuple:
    if not address_input:
        print('Getting location for the current position...')
        response = requests.get('https://api.ipdata.co?api-key=test')
        response.raise_for_status()
        payload = response.json()
        latitude, longitude = payload['latitude'], payload['longitude']
    else:
        headers = {
            'User-Agent': 'py-weather github.com/BVengerov/py-weather',
        }
        url = 'https://nominatim.openstreetmap.org/search/{}?format=json'.format(urllib.parse.quote(address_input))
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        payload = response.json()
        latitude, longitude = payload[0]["lat"], payload[0]["lon"]
    return round(float(latitude), 4), round(float(longitude), 4)


def print_current_weather(results):
    units = results['properties']['meta']['units']
    print(units)
    timeserie = results['properties']['timeseries'][0]
    forecast_time = arrow.get(timeserie['time']).humanize()
    weather = timeserie['data']['instant']['details']
    temp = str(weather['air_temperature']) + ' ' + units['air_temperature']
    pressure = str(weather['air_pressure_at_sea_level']) + ' ' + units['air_pressure_at_sea_level']
    humidity = str(weather['relative_humidity']) + ' ' + units['relative_humidity']
    wind_speed = str(weather['wind_speed']) + ' ' + units['wind_speed']
    report = '''
    Current weather conditions:
        Temperature: {}
        Air pressure: {}
        Humidity: {}
        Wind speed: {}
        Weather report obtained {}.
    '''.format(
        temp, pressure, humidity, wind_speed, forecast_time
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
