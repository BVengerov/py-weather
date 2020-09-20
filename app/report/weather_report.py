import re
from collections import namedtuple
from app.geolocation.geolocation import Geolocation
import arrow


class ParameterNames:
    air_temp = 'air_temperature'
    air_pressure = 'air_pressure_at_sea_level'
    humidity = 'relative_humidity'
    wind_speed = 'wind_speed'


class Station:
    def __init__(self, longitude, latitude, altitude):
        Location = namedtuple('Location', ['longitude', 'latitude', 'altitude'])
        self.location = Location(longitude, latitude, altitude)
        self.name = Geolocation.get_location_name_by_coordinates(longitude, latitude)


class TimeSerie:
    def __init__(self, timeserie, units):
        self.time = timeserie['time']

        # parsing and saving weather parameters of this timeserie
        data = timeserie['data']
        WeatherParameter = namedtuple('WeatherParameter', ['value', 'unit'])
        data_instant = data['instant']['details']
        params = {}
        for name in data_instant:
            params[name] = WeatherParameter(data_instant[name], units[name])
        self.params = params

        # parsing and saving forecast estimations for this timeserie
        Forecast = namedtuple('Forecast', ['period', 'summary_symbol', 'params'])
        data_forecasts = timeserie['data']
        del data_forecasts['instant']
        forecasts = []
        for forecast_period in data_forecasts:
            # forecast params are not constant, and not always present at all
            forecast_params = {}
            if 'details' in data_forecasts[forecast_period]:
                for name in data_forecasts[forecast_period]['details']:
                    forecast_params[name] = WeatherParameter(
                        data_forecasts[forecast_period]['details'][name],
                        units[name]
                    )
            forecasts.append(Forecast(
                int(re.sub(r"\D", "", forecast_period)),
                data_forecasts[forecast_period]['summary']['symbol_code'],
                sorted(forecast_params)
            ))
        self.forecasts = sorted(forecasts, key=lambda forecast: forecast.period)

    def get_param_hr(self, parameter_name):
        """Return human-readable parameter information: value with measurement units."""
        return "{} {}".format(self.params[parameter_name].value, self.params[parameter_name].unit)


class WeatherReport:
    def __init__(self, json_payload):
        self.station = Station(*json_payload['geometry']['coordinates'])

        self.timeseries = [
            TimeSerie(ts_data, json_payload['properties']['meta']['units'])
            for ts_data in json_payload['properties']['timeseries']
        ]

    def printable_temp_chart(self):
        times, temps = [], []
        for timeserie in self.timeseries:
            times.append(arrow.get(timeserie.time).to('local').format('HH:mm'))
            temps.append(timeserie.params[ParameterNames.air_temp].value)
        return '''
        Temperature chart for {}:
        | Time |{}
        | Temp |{}
        '''.format(
            self.station.name,
            " |".join(" {}".format(t) for t in times),
            "  |".join(" {}".format(t) for t in temps),
        )

    def printable_report_current(self):
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
            timeserie.get_param_hr(ParameterNames.air_temp),
            timeserie.get_param_hr(ParameterNames.air_pressure),
            timeserie.get_param_hr(ParameterNames.humidity),
            timeserie.get_param_hr(ParameterNames.wind_speed),
            self.station.name,
            self.station.location.altitude,
            arrow.get(timeserie.time).humanize()
        )
