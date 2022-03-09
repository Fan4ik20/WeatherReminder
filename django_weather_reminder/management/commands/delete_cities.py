from django.core.management import BaseCommand

from django_weather_reminder.models import City


class Command(BaseCommand):
    def handle(self, *args, **options):
        City.cities.all().delete()

        print("All cities deleted successfully.")
