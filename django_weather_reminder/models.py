from typing import Union

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MinValueValidator, MaxValueValidator

from django_weather_reminder.validators import validate_frequency

# Models Managers.


class CityManager(models.Manager):
    def country_cities(
            self, country: Union['Country', int]
    ) -> models.QuerySet['City']:
        cities = self.filter(country=country).select_related(
            'country'
        ).order_by('pk')

        return cities

    def active_cities(self) -> models.QuerySet['City']:
        active_cities = self.filter(active=True)

        return active_cities


class CurrentWeatherManager(models.Manager):
    def create_forecast(
            self, weather_status, weather_description,
            date_time, temp, feels_like, pressure, humidity,
            wind_speed, city
    ) -> 'CurrentWeather':
        current_forecast = self.create(
            weather_status=weather_status,
            weather_description=weather_description,
            date_time=date_time, temp=temp, feels_like=feels_like,
            pressure=pressure, humidity=humidity, wind_speed=wind_speed,
            city=city
        )

        return current_forecast

    def latest_current_forecast(
            self, country: Union['Country', int], city: Union['City', int]
    ) -> 'CurrentWeather':
        current_forecast = self.filter(
            city__country=country, city=city
        ).select_related(
            'city'
        ).order_by('date_time').last()

        return current_forecast


class CustomUserManager(UserManager):
    def with_subscriptions(self, frequency: int) -> models.QuerySet['User']:
        users = self.filter(
            subscriptions__frequency=frequency
        ).prefetch_related('subscriptions')

        return users

    def with_subscriptions_and_cities(
            self, frequency: int
    ) -> models.QuerySet['User']:
        users = self.filter(
            subscriptions__frequency=frequency
        ).prefetch_related(
            'subscriptions', 'city_subscriptions',
            'city_subscriptions__country'
        )

        return users

    def check_exists(self, username: str) -> bool:
        return self.filter(username=username).exists()


class SubscriptionManager(models.Manager):
    def user_subscriptions(self, user: 'User'):
        return self.filter(user=user).select_related('user', 'city')


# Models.


class User(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)

    city_subscriptions = models.ManyToManyField(
        'City', through='Subscription', related_name='subscribed_users',
    )

    users = CustomUserManager()


class City(models.Model):
    name = models.CharField(max_length=100)
    lat = models.FloatField()
    lon = models.FloatField()

    active = models.BooleanField(default=False)

    country = models.ForeignKey(
        'Country', on_delete=models.CASCADE, related_name='cities'
    )

    cities = CityManager()

    def __str__(self):
        return f'{self.name} | {self.country.name}'


class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscriptions'
    )
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name='subscriptions'
    )

    frequency = models.PositiveIntegerField(validators=[validate_frequency])

    subscriptions = SubscriptionManager()


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=2, unique=True)

    countries = models.Manager()

    def __str__(self):
        return self.name


class AbstractWeatherForecast(models.Model):
    weather_description = models.CharField(max_length=100)
    weather_status = models.CharField(max_length=20)

    pressure = models.IntegerField()
    humidity = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    wind_speed = models.IntegerField()

    class Meta:
        abstract = True


class CurrentWeather(AbstractWeatherForecast):
    temp = models.FloatField()
    feels_like = models.FloatField()

    date_time = models.DateTimeField()

    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name='current_forecasts'
    )

    forecasts = CurrentWeatherManager()
