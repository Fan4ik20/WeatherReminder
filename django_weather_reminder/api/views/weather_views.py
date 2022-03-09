from rest_framework import viewsets, permissions

from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from django_weather_reminder.api.serializers.weather_serializers import (
    CitySerializer, CountrySerializer, SubscriptionSerializer
)
from django_weather_reminder.models import (
    City, Country, Subscription
)
from django_weather_reminder.api.permissions import IsUserSubscription


class CountryViewSet(viewsets.ModelViewSet):
    """
    list:
    Returns a list of available country.

    retrieve:
    Returns a particular country. If not exists - 404 error.
    """

    filter_backends = SearchFilter,
    search_fields = 'name',

    queryset = Country.countries.all()
    serializer_class = CountrySerializer


class CityViewSet(viewsets.ModelViewSet):
    """
    list:
    Returns a list of available cities.

    retrieve:
    Returns a particular cities. If not exists - 404 error.
    """

    filter_backends = DjangoFilterBackend, SearchFilter
    filterset_fields = 'active',
    search_fields = 'name',

    serializer_class = CitySerializer

    def get_queryset(self):
        city_id = self.kwargs['country_pk']

        return City.cities.country_cities(city_id)


class UserSubscriptionViewSet(viewsets.ModelViewSet):
    """
    list:
    Returns a list of user's subscription.

    retrieve:
    Returns a particular subscription. If not exists - 404 error.

    post:
    Takes a city and frequency parameters. Creates a new user's subscription.

    patch:
    Updates a user's existent subscription.
    """

    filter_backends = OrderingFilter,
    ordering_fields = 'frequency',

    permission_classes = permissions.IsAuthenticated, IsUserSubscription

    serializer_class = SubscriptionSerializer

    def perform_destroy(self, instance):
        instance.delete()

        if not instance.city.subscriptions.count():
            instance.city.active = False
            instance.city.save()

    def get_queryset(self):
        users_subscriptions = (
            Subscription.subscriptions.user_subscriptions(
                self.request.user
            )
        )

        return users_subscriptions
