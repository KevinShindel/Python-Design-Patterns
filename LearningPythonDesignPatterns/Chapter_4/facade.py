import datetime
import json
import pickle
from functools import reduce
from urllib.request import urlopen


class WeatherProvider:
    """ instance for make api call """
    # https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={API key}

    def __init__(self):
        self.__api_url = 'https://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&appid={}'
        self.key = 'cf122d113306493f822fc5dab94058c7'

    def get_weather(self, lat, lon):
        url = self.__api_url.format(lat, lon, self.key)
        return urlopen(url).read()


class Parser:
    """ instance for parse data """

    @staticmethod
    def parse_web_data(weather_data: str):
        parsed = json.loads(weather_data)
        start_date = None
        result = []
        for data in parsed['list']:
            date = datetime.datetime.strptime(data['dt_txt'], '%Y-%m-%d %H:%M:%S')
            start_date = start_date or date
            if start_date.day != date.day:
                return result
            result.append(data['main']['temp'])


class Cache:
    """ instance to save / load pickle object """

    def __init__(self, filename):
        self.__filename = filename

    def save(self, obj):
        with open(self.__filename, 'w') as handler:
            dct = {
                'obj': obj,
                'expired': datetime.datetime.utcnow() + datetime.timedelta(hours=3)
            }
            pickle.dump(dct, handler)

    def load(self):
        try:
            with open(self.__filename, 'r') as handler:
                obj = pickle.load(handler)
                if obj['expired'] > datetime.datetime.utcnow():
                    return obj['obj']
        except IOError:
            pass


class Converter:
    """ instance for convert from F to C temperature """

    @staticmethod
    def from_kelvin_to_celsius(value):
        return value - 273.15


class Weather:

    def __init__(self, data):
        self.__temperature = reduce(lambda x, y: x+y, data) / len(data)

    @property
    def temperature(self):
        return self.__temperature


class Facade:
    """ instance to hide all logic """

    @staticmethod
    def get_forecast(lat, lon):
        cache = Cache('myfile')
        cache_result = cache.load()
        if cache_result:
            return cache_result
        else:
            weather_provide = WeatherProvider()
            weather_data = weather_provide.get_weather(lat, lon)
            parser = Parser()
            parsed_data = parser.parse_web_data(weather_data)
            weather = Weather(parsed_data)
            converter = Converter()
            t_celsius = converter.from_kelvin_to_celsius(weather.temperature)
            cache.save(t_celsius)
            return t_celsius


if __name__ == '__main__':
    # example of using Facade pattern [ hide included logic ]
    facade = Facade()
    facade.get_forecast(46.65581, 32.6178)
