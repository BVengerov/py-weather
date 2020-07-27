#!/usr/bin/env python3
import arrow
import sys
import requests
from geolocation import Geolocation
from weather_source import WeatherAPI


def print_current_weather(results):
    # get station location
    station_coordinates = results['geometry']['coordinates']
    station_lon, station_lat, station_alt = station_coordinates
    station_name = Geolocation.get_location_name_by_coordinates(station_lon, station_lat)

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
        Station: {} [{} m]
        Weather report obtained {}.
    '''.format(
        temp, pressure, humidity, wind_speed, station_name, station_alt, forecast_time
    )
    print(report)


def get_weather(address: str):
    """GET WEATHER APP"""
    if address:
        longitude, latitude = Geolocation.get_coordinates_for_address(address)
    else:
        longitude, latitude = Geolocation.get_coordinates_by_ip()
    print_current_weather(WeatherAPI.get_current_forecast(longitude, latitude))


if __name__ == '__main__':
    try:
        search_address = sys.argv[1]
    except IndexError:
        search_address = ''
    get_weather(search_address)
