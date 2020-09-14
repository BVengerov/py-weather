#!/usr/bin/env python3
import sys
from geolocation import Geolocation
from weather_source import WeatherAPI


def get_weather(address: str):
    """GET WEATHER APP"""
    if address:
        longitude, latitude = Geolocation.get_coordinates_for_address(address)
    else:
        longitude, latitude = Geolocation.get_coordinates_by_ip()
    weather_report = WeatherAPI.get_weather_report(longitude, latitude)
    print(weather_report.printable_report_current())


if __name__ == '__main__':
    try:
        search_address = sys.argv[1]
    except IndexError:
        search_address = ''
    get_weather(search_address)
