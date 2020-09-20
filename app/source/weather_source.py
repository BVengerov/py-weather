import requests
from app.report.weather_report import WeatherReport


class WeatherAPI:
    @classmethod
    def get_weather_report(cls, longitude, latitude):
        headers = {
            'User-Agent': 'py-weather github.com/BVengerov/py-weather',
        }
        response = requests.get('https://api.met.no/weatherapi/locationforecast/2.0/complete?lon={}&lat={}'.format(
            round(float(longitude), 4), round(float(latitude), 4)
        ), headers=headers)
        response.raise_for_status()
        return WeatherReport(response.json())
