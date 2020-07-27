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
        longitude, latitude = payload['longitude'], payload['latitude']
    else:
        url = 'https://nominatim.openstreetmap.org/search/{}?format=json'.format(urllib.parse.quote(address_input))
        response = requests.get(url)
        response.raise_for_status()
        payload = response.json()
        longitude, latitude = payload[0]["lon"], payload[0]["lat"]
    return round(float(longitude), 4), round(float(latitude), 4)


def print_current_weather(results):
    # get station location
    station_coordinates = results['geometry']['coordinates']
    station_lon, station_lat = station_coordinates[0], station_coordinates[1]
    url = 'https://nominatim.openstreetmap.org/reverse/?lon={}&lat={}&zoom=14&format=json'.format(
        station_lon, station_lat
    )
    response = requests.get(url)
    response.raise_for_status()
    station_name = response.json()['display_name']

    # parse metrics and units
    units = results['properties']['meta']['units']
    timeserie = results['properties']['timeseries'][0]
    forecast_time = arrow.get(timeserie['time']).humanize()
    weather = timeserie['data']['instant']['details']
    temp = str(weather['air_temperature']) + ' ' + units['air_temperature']
    pressure = str(weather['air_pressure_at_sea_level']) + ' ' + units['air_pressure_at_sea_level']
    humidity = str(weather['relative_humidity']) + ' ' + units['relative_humidity']
    wind_speed = str(weather['wind_speed']) + ' ' + units['wind_speed']

    # format and print
    report = '''
    Current weather conditions:
        Temperature: {}
        Air pressure: {}
        Humidity: {}
        Wind speed: {}
        Station: {}
        Weather report obtained {}.
    '''.format(
        temp, pressure, humidity, wind_speed, station_name, forecast_time
    )
    print(report)


def get_weather(address: str):
    """GET WEATHER APP"""

    headers = {
        'User-Agent': 'py-weather github.com/BVengerov/py-weather',
    }
    response = requests.get('https://api.met.no/weatherapi/locationforecast/2.0/complete?lon={}&lat={}'.format(
        *get_coordinates(address)
    ), headers=headers)

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
