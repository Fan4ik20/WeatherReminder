from unittest import mock

from django.test import TestCase

from django_weather_reminder.tests import factories
from django_weather_reminder.tasks import send_mail_every_n_hours


class TestTasks(TestCase):
    def setUp(self) -> None:
        self.country = factories.CountryFactory()

        self.active_cities = [
            factories.CityFactory(active=True, country=self.country)
            for _ in range(5)
        ]

    @mock.patch(
        'django_weather_reminder.tasks.service.send_users_weather_forecast'
    )
    def test_send_users_weather_forecast_success(self, send_mail) -> None:
        send_mail_every_n_hours(3)

        send_mail.assert_called_with(3)
