import random
from datetime import datetime

import factory

from django_weather_reminder import models


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('user_name')
    email = factory.Faker('ascii_email')

    password = factory.Faker('password')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)

        return manager.create_user(*args, **kwargs)

    class Meta:
        model = models.User


class CountryFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('country')
    code = factory.Faker('country_code')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)

        return manager.create(*args, **kwargs)

    class Meta:
        model = models.Country


class CityFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('city')
    lat = factory.Faker('latitude')
    lon = factory.Faker('longitude')

    country = factory.SubFactory(CountryFactory)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)

        return manager.create(*args, **kwargs)

    class Meta:
        model = models.City


class SubscriptionFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    city = factory.SubFactory(CityFactory)

    frequency = 3

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)

        return manager.create(*args, **kwargs)

    class Meta:
        model = models.Subscription


class UserWithSubscriptionsFactory(UserFactory):
    subscription = factory.RelatedFactory(SubscriptionFactory)


class CurrentWeatherFactory(factory.django.DjangoModelFactory):
    temp = random.uniform(-5, 5)
    feels_like = temp + 1.2

    pressure = random.randint(1, 1000)
    humidity = random.randint(0, 100)
    wind_speed = random.randint(0, 100)

    weather_description = 'clouds is here'
    weather_status = 'clouds'

    date_time = datetime.now()

    city = factory.SubFactory(CityFactory)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)

        return manager.create(*args, **kwargs)

    class Meta:
        model = models.CurrentWeather
