import os
from datetime import datetime
from typing import Literal

from django.core.mail import send_mail

from django_weather_reminder.models import City, User
from django_weather_reminder.models import CurrentWeather as WeatherForecast
from django_weather_reminder.weather_db.fillers import CurrentWeather


def fill_weather_active_cities() -> None:
    filler = CurrentWeather()

    active_cities = City.cities.active_cities()

    for city in active_cities:
        filler.fill_city_weather(city)


def datetime_to_readable_format(date_time: datetime) -> str:
    return date_time.strftime('%m/%d/%Y %H:%M')


def _send_weather_forecast_mail(
        user: User, forecast: WeatherForecast
) -> None:
    send_mail(
        f'Weather in {forecast.city.name}',
        (
            'Quick report:\n'
            f'Weather status - {forecast.weather_status}\n'
            f'Brief description - {forecast.weather_description}\n'
            f'Temperature - {forecast.temp}\n'
            f'Feels like - {forecast.feels_like}\n'
            f'Pressure - {forecast.pressure}\n'
            f'Humidity - {forecast.humidity}\n'
            f'Wind Speed - {forecast.wind_speed}\n'
            'Forecast given as of '
            f'{datetime_to_readable_format(forecast.date_time)} UTC'
        ),
        os.getenv('EMAIL_HOST_USER'),
        (user.email,)
    )


Frequency = Literal[1, 3, 6, 12, 24]


def send_users_weather_forecast(subscription_frequency: Frequency) -> None:
    users = User.users.with_subscriptions_and_cities(subscription_frequency)

    if not users:
        return None

    for user in users:
        for city in user.city_subscriptions.all():
            last_forecast = WeatherForecast.forecasts.latest_current_forecast(
                city.country, city
            )

            _send_weather_forecast_mail(user, last_forecast)
