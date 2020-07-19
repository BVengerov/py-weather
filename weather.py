"""WEATHER APP

Usage:
    weather.py <address>

Options:
    <address> Place to search weather for.
"""

from docopt import docopt
from pip._vendor import requests


def search_weather(address):
    print("You're searching the weather in {}.".format(address))
    import urllib.parse

    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) + '?format=json'

    response = requests.get(url).json()
    latitude = response[0]["lat"]
    longitude = response[0]["lon"]

    # Getting location for current position
    # r = requests.get('https://api.ipdata.co?api-key=test').json()
    # print(r)

    result = requests.get('https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={}&lon={}'.format(
        latitude, longitude
    ))
    print(result.json())


if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.0.1')
    if arguments['<address>']:
        search_weather(address=arguments['<address>'])
    else:
        print(arguments)
