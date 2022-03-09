from typing import Type

from django.core.management import BaseCommand

from django_weather_reminder.weather_db.fillers import (
    UkraineCitiesFromJson
)
from django_weather_reminder.models import Country


class Command(BaseCommand):
    help = 'This command populates the database with countries and cities.'

    @staticmethod
    def create_ukraine() -> Type[Country]:
        try:
            ukraine = Country.countries.get(name='Ukraine', code='UA')
        except Country.DoesNotExist:
            ukraine = Country.countries.create(name='Ukraine', code='UA')

        return ukraine

    @classmethod
    def fill_cities(cls):
        locations_json = (
            'django_weather_reminder/weather_db/'
            'locations_data/ua_cities.json'
        )

        cls.create_ukraine()

        ukraine_parser = UkraineCitiesFromJson(locations_json)

        ukraine_parser.write_cities_to_db()

    def handle(self, *args, **options):
        self.fill_cities()
