import json
import os

from django_weather_reminder import models
from django_weather_reminder.openweathermap.parser import OpenWeatherMapParser
from django_weather_reminder.weather_db.support import converters


class UkraineCitiesFromJson:
    def __init__(self, filepath: str):
        self._filepath = filepath
        self._locations_data: None | list = None
        self._cities_data: list[tuple] = []

        if not os.path.exists(filepath):
            raise ValueError('Given directory doesn\'t exists!')

    def _read_file(self) -> None:
        with open(self._filepath, encoding='utf-8') as file:
            data = json.load(file)

            self._locations_data = data

    def _parse_cities_data(self) -> None:
        data_length = len(self._locations_data)

        for i, data in enumerate(self._locations_data):
            print(f'Processing {i + 1} location of {data_length}.')

            if data['type'] != 'CITY':
                continue

            if not (lat := data['lat']) or not (lon := data['lng']):
                continue

            self._cities_data.append(
                (data['name']['en'], lat, lon)
            )

    def _create_city_objects(self) -> None:
        try:
            ukraine = models.Country.countries.get(name='Ukraine')
        except models.Country.DoesNotExist:
            raise ValueError('First of all - create  Ukraine instance!')

        cities_length = len(self._cities_data)
        for i, city_data in enumerate(self._cities_data):
            print(f'Adding a {i + 1} city of {cities_length} to the database.')

            city_name, lat, lon = city_data

            models.City.cities.create(
                name=city_name, lat=lat, lon=lon, country=ukraine
            )

        print('The filling was successful.')

    def write_cities_to_db(self) -> None:
        self._read_file()
        self._parse_cities_data()
        self._create_city_objects()


class CurrentWeather:
    def __init__(self):
        self._parser = OpenWeatherMapParser()

    def _get_weather_data(self, city) -> dict:
        current_weather_data = self._parser.parse_city_current_weather(
            city.lat, city.lon
        )

        return current_weather_data

    @staticmethod
    def _create_weather(
            weather_data: dict, city: models.City
    ) -> models.CurrentWeather:
        forecast_date_time = converters.convert_unix_time_to_datetime(
            weather_data['date_time']
        )
        return models.CurrentWeather.forecasts.create_forecast(
            weather_data['weather_status'],
            weather_data['weather_description'], forecast_date_time,
            weather_data['temp'], weather_data['feels_like'],
            weather_data['pressure'], weather_data['humidity'],
            weather_data['wind_speed'], city
        )

    def fill_city_weather(self, city: models.City) -> None:
        current_weather_data = self._get_weather_data(city)
        self._create_weather(current_weather_data, city)
