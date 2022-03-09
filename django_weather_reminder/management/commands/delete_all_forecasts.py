from django.core.management import BaseCommand

from django_weather_reminder.models import CurrentWeather


class Command(BaseCommand):
    def handle(self, *args, **options):
        CurrentWeather.forecasts.all().delete()

        print("All weather forecasts deleted successfully.")
