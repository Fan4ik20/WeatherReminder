from unittest import mock
from datetime import datetime

from django.test import TestCase
from django.core import mail

from django_weather_reminder.service import (
    fill_weather_active_cities, _send_weather_forecast_mail,
    datetime_to_readable_format, send_users_weather_forecast
)
from django_weather_reminder.tests import factories
from django_weather_reminder import models

returned_json = {
    'weather_status': 'Clouds', 'weather_description': 'overcast clouds',
    'temp': 0.02, 'feels_like': -2.81, 'date_time': 1645221843,
    'pressure': 1012, 'humidity': 90, 'wind_speed': 2.32
}


class TestService(TestCase):
    def setUp(self) -> None:
        self.country = factories.CountryFactory()

        self.active_cities = [
            factories.CityFactory(active=True, country=self.country)
            for _ in range(5)
        ]

    @mock.patch(
        'django_weather_reminder.service.CurrentWeather._get_weather_data',
        return_value=returned_json
    )
    def test_fill_weather_active_cities(self, get_weather) -> None:
        fill_weather_active_cities()

        forecasts_count = models.CurrentWeather.forecasts.all().count()

        forecast = models.CurrentWeather.forecasts.first()

        self.assertEqual(
            forecast.weather_status, returned_json['weather_status']
        )
        self.assertEqual(
            forecast.temp, returned_json['temp']
        )
        self.assertEqual(forecast.pressure, returned_json['pressure'])

        self.assertEqual(forecasts_count, len(self.active_cities))

    def test_send_weather_forecast_mail(self):
        test_city = self.active_cities[0]
        test_forecast = factories.CurrentWeatherFactory(city=test_city)
        test_user = factories.UserFactory(email='test@test.com')

        _send_weather_forecast_mail(
            test_user, test_forecast
        )

        expected_subject = f'Weather in {test_forecast.city.name}'

        expected_message = (
            'Quick report:',
            f'Weather status - {test_forecast.weather_status}',
            f'Brief description - {test_forecast.weather_description}',
            f'Temperature - {test_forecast.temp}',
            f'Feels like - {test_forecast.feels_like}',
            f'Pressure - {test_forecast.pressure}',
            f'Humidity - {test_forecast.humidity}',
            f'Wind Speed - {test_forecast.wind_speed}',
            'Forecast given as of ',
            f'{datetime_to_readable_format(test_forecast.date_time)} UTC'
        )

        self.assertEqual(mail.outbox[0].subject, expected_subject)
        self.assertEqual(mail.outbox[0].to[0], test_user.email)

        for message in expected_message:
            with self.subTest():
                self.assertIn(message, str(mail.outbox[0].message()))

    def test_send_users_weather_forecast_with_empty_users(self):
        self.assertIsNone(send_users_weather_forecast(1))

    @staticmethod
    def _create_subscription(
            test_user: models.User, city: models.City, frequency: int
    ) -> None:
        models.Subscription.subscriptions.create(
            user=test_user, city=city, frequency=frequency
        )

    @mock.patch('django_weather_reminder.service._send_weather_forecast_mail')
    def test_send_users_weather_forecast(self, send_mail):
        test_city = factories.CityFactory()

        test_forecasts = [
            factories.CurrentWeatherFactory(city=test_city),
            factories.CurrentWeatherFactory(
                city=test_city, date_time=datetime.now()
            )
        ]

        test_users = [factories.UserFactory(), factories.UserFactory()]

        self._create_subscription(test_users[0], test_city, 1)
        self._create_subscription(test_users[1], test_city, 3)

        send_users_weather_forecast(1)
        send_mail.assert_called_with(test_users[0], test_forecasts[1])

        send_users_weather_forecast(3)
        send_mail.assert_called_with(test_users[1], test_forecasts[1])
