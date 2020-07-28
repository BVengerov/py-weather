import re
from collections import namedtuple
from geolocation import Geolocation
from typing import NamedTuple


class Station:
    def __init__(self, longitude, latitude, altitude):
        Location = namedtuple('Location', ['longitude', 'latitude', 'altitude'])
        self.location = Location(longitude, latitude, altitude)
        self.name = Geolocation.get_location_name_by_coordinates(longitude, latitude)


class TimeSerie:
    def __init__(self, timeserie, units):
        self.time = timeserie['time']

        data = timeserie['data']
        WeatherParameter = namedtuple('WeatherParameter', ['value', 'unit'])
        data_instant = data['instant']['details']
        params = {}
        for name in data_instant:
            params[name] = WeatherParameter(data_instant[name], units[name])
        self.params = params

        Forecast = namedtuple('Forecast', ['period', 'summary_symbol', 'params'])
        data_forecasts = timeserie['data']
        del data_forecasts['instant']
        forecasts = []
        for forecast_period in data_forecasts:
            forecast_params = {}
            if 'details' in data_forecasts[forecast_period]:
                for name in data_forecasts[forecast_period]['details']:
                    forecast_params[name] = WeatherParameter(data_forecasts[forecast_period]['details'][name], units[name])
            forecasts.append(Forecast(
                int(re.sub(r"\D", "", forecast_period)),
                data_forecasts[forecast_period]['summary']['symbol_code'],
                sorted(forecast_params)
            ))
        self.forecasts = sorted(forecasts, key=lambda forecast: forecast.period)

    def get_param_hr(self, parameter_name):
        return "{} {}".format(self.params[parameter_name].value, self.params[parameter_name].unit)


class WeatherReport:
    def __init__(self, json_payload):
        self.station = Station(*json_payload['geometry']['coordinates'])

        self.timeseries = [
            TimeSerie(ts_data, json_payload['properties']['meta']['units'])
            for ts_data in json_payload['properties']['timeseries']
        ]


    def __str__(self):

        # timeserie = results['properties']['timeseries'][0]
        # forecast_time = arrow.get(timeserie['time']).humanize()
        # weather = timeserie['data']['instant']['details']
        # temp = str(weather['air_temperature']) + ' ' + units['air_temperature']
        # pressure = str(weather['air_pressure_at_sea_level']) + ' ' + units['air_pressure_at_sea_level']
        # humidity = str(weather['relative_humidity']) + ' ' + units['relative_humidity']
        # wind_speed = str(weather['wind_speed']) + ' ' + units['wind_speed']
        #
        timeserie = self.timeseries[0]
        return '''
        Current weather conditions:
            Temperature: {}
            Air pressure: {}
            Humidity: {}
            Wind speed: {}
            Station: {} [{} m]
            Weather report obtained {}.
        '''.format(
            timeserie.get_param_hr('air_temperature'),
            timeserie.get_param_hr('air_pressure_at_sea_level'),
            timeserie.get_param_hr('relative_humidity'),
            timeserie.get_param_hr('wind_speed'),
            self.station.name,
            self.station.location.altitude,
            timeserie.time
        )
