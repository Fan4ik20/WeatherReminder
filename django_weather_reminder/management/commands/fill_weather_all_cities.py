import warnings

from django.core.management import BaseCommand

from django_weather_reminder.models import City
from django_weather_reminder.weather_db.fillers import CurrentWeather


class Command(BaseCommand):
    def handle(self, *args, **options):
        cities = City.cities.all()
        cities_length = len(cities)

        weather_parser = CurrentWeather()

        for i, city in enumerate(cities):
            print(f'Filling a {i + 1} of {cities_length} cities')
            with warnings.catch_warnings():
                weather_parser.fill_city_weather(city)

        print('The filling was successful.')
