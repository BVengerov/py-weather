import sys

import requests


def search_weather(address):
    print("You're searching the weather in {}.".format(address))
    import urllib.parse

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
    search_weather(sys.argv[1])
